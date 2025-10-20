"""
Cliente S3 para gestión de imágenes en Amazon S3.
"""
import os
import logging
from typing import Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from flask import current_app

logger = logging.getLogger(__name__)


class S3Client:
    """Cliente para interactuar con Amazon S3."""
    
    def __init__(self, bucket: str = None, region: str = None):
        """
        Inicializa el cliente S3.
        
        Args:
            bucket: Nombre del bucket S3
            region: Región de AWS
        """
        self.bucket = bucket or current_app.config.get('S3_BUCKET', '')
        self.region = region or current_app.config.get('S3_REGION', 'us-east-1')
        self.use_presigned = current_app.config.get('USE_S3_PRESIGNED', False)
        self.public_base_url = current_app.config.get('S3_PUBLIC_BASE_URL', '')
        self.presigned_expiration = current_app.config.get('PRESIGNED_URL_EXPIRATION', 3600)
        
        self._client = None
    
    @property
    def client(self):
        """Lazy loading del cliente boto3."""
        if self._client is None:
            try:
                # Intenta usar credenciales de variables de entorno o perfil
                self._client = boto3.client(
                    's3',
                    region_name=self.region,
                    aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID') or None,
                    aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY') or None,
                    aws_session_token=current_app.config.get('AWS_SESSION_TOKEN') or None
                )
            except Exception as e:
                logger.error(f"Error al crear cliente S3: {e}")
                raise
        return self._client
    
    def get_public_url(self, key: str) -> str:
        """
        Construye URL pública para un objeto S3.
        
        Args:
            key: Clave del objeto en S3
            
        Returns:
            URL pública del objeto
        """
        if self.public_base_url:
            # Usar URL base personalizada
            return f"{self.public_base_url.rstrip('/')}/{key}"
        else:
            # Construir URL estándar de S3
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
    
    def get_presigned_url(self, key: str, expiration: int = None) -> Optional[str]:
        """
        Genera una URL presignada para un objeto S3.
        
        Args:
            key: Clave del objeto en S3
            expiration: Tiempo de expiración en segundos (default: config)
            
        Returns:
            URL presignada o None si hay error
        """
        if expiration is None:
            expiration = self.presigned_expiration
        
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket,
                    'Key': key
                },
                ExpiresIn=expiration
            )
            return url
        except NoCredentialsError:
            logger.error("No se encontraron credenciales de AWS")
            return None
        except ClientError as e:
            logger.error(f"Error al generar URL presignada: {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado al generar URL presignada: {e}")
            return None
    
    def get_image_url(self, key: str) -> Optional[str]:
        """
        Obtiene la URL de una imagen según la configuración.
        
        Args:
            key: Clave de la imagen en S3
            
        Returns:
            URL de la imagen (pública o presignada) o None
        """
        if not self.bucket:
            logger.warning("S3_BUCKET no está configurado")
            return None
        
        if self.use_presigned:
            return self.get_presigned_url(key)
        else:
            return self.get_public_url(key)
    
    def check_object_exists(self, key: str) -> bool:
        """
        Verifica si un objeto existe en S3.
        
        Args:
            key: Clave del objeto
            
        Returns:
            True si existe, False en caso contrario
        """
        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            logger.error(f"Error al verificar objeto: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al verificar objeto: {e}")
            return False


def get_s3_client() -> S3Client:
    """
    Factory function para obtener una instancia del cliente S3.
    
    Returns:
        Instancia de S3Client
    """
    return S3Client()
