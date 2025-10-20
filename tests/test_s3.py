"""
Tests para el cliente S3.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError, NoCredentialsError


class TestS3Client:
    """Tests para el cliente S3."""
    
    @patch('app.storage.s3.boto3.client')
    def test_get_public_url_with_bucket_and_region(self, mock_boto_client, app):
        """Verifica que se construye correctamente la URL pública."""
        with app.app_context():
            app.config['S3_BUCKET'] = 'test-bucket'
            app.config['S3_REGION'] = 'us-east-1'
            app.config['USE_S3_PRESIGNED'] = False
            app.config['S3_PUBLIC_BASE_URL'] = ''
            
            from app.storage.s3 import S3Client
            
            s3_client = S3Client()
            url = s3_client.get_public_url('pokeneas/test.jpg')
            
            expected_url = 'https://test-bucket.s3.us-east-1.amazonaws.com/pokeneas/test.jpg'
            assert url == expected_url
    
    @patch('app.storage.s3.boto3.client')
    def test_get_public_url_with_custom_base(self, mock_boto_client, app):
        """Verifica que se usa la URL base personalizada si está configurada."""
        with app.app_context():
            app.config['S3_BUCKET'] = 'test-bucket'
            app.config['S3_PUBLIC_BASE_URL'] = 'https://cdn.example.com'
            app.config['USE_S3_PRESIGNED'] = False
            
            from app.storage.s3 import S3Client
            
            s3_client = S3Client()
            url = s3_client.get_public_url('pokeneas/test.jpg')
            
            expected_url = 'https://cdn.example.com/pokeneas/test.jpg'
            assert url == expected_url
    
    @patch('app.storage.s3.boto3.client')
    def test_get_presigned_url_success(self, mock_boto_client, app):
        """Verifica que se genera correctamente una URL presignada."""
        with app.app_context():
            app.config['S3_BUCKET'] = 'test-bucket'
            app.config['USE_S3_PRESIGNED'] = True
            
            # Mock del cliente boto3
            mock_s3 = MagicMock()
            mock_s3.generate_presigned_url.return_value = 'https://presigned-url.example.com'
            mock_boto_client.return_value = mock_s3
            
            from app.storage.s3 import S3Client
            
            s3_client = S3Client()
            url = s3_client.get_presigned_url('pokeneas/test.jpg', expiration=300)
            
            assert url == 'https://presigned-url.example.com'
            mock_s3.generate_presigned_url.assert_called_once()
    
    @patch('app.storage.s3.boto3.client')
    def test_get_presigned_url_no_credentials(self, mock_boto_client, app):
        """Verifica manejo de error cuando no hay credenciales."""
        with app.app_context():
            app.config['S3_BUCKET'] = 'test-bucket'
            app.config['USE_S3_PRESIGNED'] = True
            
            # Mock del cliente boto3 que lanza NoCredentialsError
            mock_s3 = MagicMock()
            mock_s3.generate_presigned_url.side_effect = NoCredentialsError()
            mock_boto_client.return_value = mock_s3
            
            from app.storage.s3 import S3Client
            
            s3_client = S3Client()
            url = s3_client.get_presigned_url('pokeneas/test.jpg')
            
            assert url is None
    
    @patch('app.storage.s3.boto3.client')
    def test_get_presigned_url_client_error(self, mock_boto_client, app):
        """Verifica manejo de ClientError."""
        with app.app_context():
            app.config['S3_BUCKET'] = 'test-bucket'
            app.config['USE_S3_PRESIGNED'] = True
            
            # Mock del cliente boto3 que lanza ClientError
            mock_s3 = MagicMock()
            error_response = {'Error': {'Code': 'AccessDenied', 'Message': 'Access Denied'}}
            mock_s3.generate_presigned_url.side_effect = ClientError(error_response, 'generate_presigned_url')
            mock_boto_client.return_value = mock_s3
            
            from app.storage.s3 import S3Client
            
            s3_client = S3Client()
            url = s3_client.get_presigned_url('pokeneas/test.jpg')
            
            assert url is None
    
    @patch('app.storage.s3.boto3.client')
    def test_get_image_url_public_mode(self, mock_boto_client, app):
        """Verifica que get_image_url usa modo público cuando está configurado."""
        with app.app_context():
            app.config['S3_BUCKET'] = 'test-bucket'
            app.config['S3_REGION'] = 'us-west-2'
            app.config['USE_S3_PRESIGNED'] = False
            app.config['S3_PUBLIC_BASE_URL'] = ''
            
            from app.storage.s3 import S3Client
            
            s3_client = S3Client()
            url = s3_client.get_image_url('pokeneas/test.jpg')
            
            assert url is not None
            assert 'test-bucket.s3.us-west-2.amazonaws.com' in url
    
    @patch('app.storage.s3.boto3.client')
    def test_get_image_url_presigned_mode(self, mock_boto_client, app):
        """Verifica que get_image_url usa modo presignado cuando está configurado."""
        with app.app_context():
            app.config['S3_BUCKET'] = 'test-bucket'
            app.config['USE_S3_PRESIGNED'] = True
            
            # Mock del cliente boto3
            mock_s3 = MagicMock()
            mock_s3.generate_presigned_url.return_value = 'https://presigned.example.com'
            mock_boto_client.return_value = mock_s3
            
            from app.storage.s3 import S3Client
            
            s3_client = S3Client()
            url = s3_client.get_image_url('pokeneas/test.jpg')
            
            assert url == 'https://presigned.example.com'
    
    @patch('app.storage.s3.boto3.client')
    def test_get_image_url_no_bucket_configured(self, mock_boto_client, app):
        """Verifica que retorna None cuando no hay bucket configurado."""
        with app.app_context():
            app.config['S3_BUCKET'] = ''
            
            from app.storage.s3 import S3Client
            
            s3_client = S3Client()
            url = s3_client.get_image_url('pokeneas/test.jpg')
            
            assert url is None


class TestS3Service:
    """Tests de integración para el servicio de Pokeneas con S3."""
    
    @patch('app.storage.s3.boto3.client')
    def test_pokeneas_service_resolves_image_url(self, mock_boto_client, app):
        """Verifica que el servicio de Pokeneas resuelve URLs de imágenes."""
        with app.app_context():
            app.config['S3_BUCKET'] = 'test-bucket'
            app.config['USE_S3_PRESIGNED'] = False
            
            from app.services.pokeneas_service import PokeneasService
            
            service = PokeneasService()
            pokenea = service.get_pokenea_for_view()
            
            # Debe tener imagen_url
            assert 'imagen_url' in pokenea
            # Puede ser None si el bucket no está configurado, pero el campo debe existir
            if app.config['S3_BUCKET']:
                assert pokenea['imagen_url'] is not None
