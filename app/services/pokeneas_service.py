"""
Servicio de lógica de negocio para Pokeneas.
"""
import random
import socket
from typing import Dict, Optional
from flask import current_app
from app.data.pokeneas import POKENEAS_DATA
from app.storage.s3 import get_s3_client


class PokeneasService:
    """Servicio para manejar la lógica de Pokeneas."""
    
    def __init__(self):
        """Inicializa el servicio."""
        self.pokeneas = POKENEAS_DATA
    
    def get_random_pokenea(self) -> Dict:
        """
        Selecciona un Pokenea aleatorio del arreglo.
        
        Returns:
            Diccionario con los datos del Pokenea
        """
        return random.choice(self.pokeneas)
    
    def get_container_id(self) -> str:
        """
        Obtiene el ID del contenedor actual.
        
        En Docker, el hostname del contenedor es su ID.
        
        Returns:
            ID del contenedor (hostname)
        """
        try:
            return socket.gethostname()
        except Exception as e:
            current_app.logger.error(f"Error al obtener container ID: {e}")
            return "unknown"
    
    def resolve_image_url(self, image_key: str) -> Optional[str]:
        """
        Resuelve la URL de una imagen desde S3.
        
        Args:
            image_key: Clave de la imagen en S3 (ej: "pokeneas/arepa-001.jpg")
            
        Returns:
            URL de la imagen o None si no se puede resolver
        """
        try:
            s3_client = get_s3_client()
            return s3_client.get_image_url(image_key)
        except Exception as e:
            current_app.logger.error(f"Error al resolver URL de imagen: {e}")
            return None
    
    def get_pokenea_for_api(self) -> Dict:
        """
        Obtiene un Pokenea aleatorio formateado para la API REST.
        
        Returns:
            Diccionario con: id, nombre, altura, habilidad, container_id
        """
        pokenea = self.get_random_pokenea()
        container_id = self.get_container_id()
        
        return {
            "id": pokenea["id"],
            "nombre": pokenea["nombre"],
            "altura": pokenea["altura"],
            "habilidad": pokenea["habilidad"],
            "container_id": container_id
        }
    
    def get_pokenea_for_view(self) -> Dict:
        """
        Obtiene un Pokenea aleatorio formateado para la vista HTML.
        
        Returns:
            Diccionario con todos los campos incluyendo imagen_url y container_id
        """
        pokenea = self.get_random_pokenea()
        container_id = self.get_container_id()
        
        # Resolver URL de la imagen
        image_url = self.resolve_image_url(pokenea["imagen"])
        
        return {
            "id": pokenea["id"],
            "nombre": pokenea["nombre"],
            "altura": pokenea["altura"],
            "habilidad": pokenea["habilidad"],
            "imagen_url": image_url,
            "frase_filosofica": pokenea["frase_filosofica"],
            "container_id": container_id
        }


def get_pokeneas_service() -> PokeneasService:
    """
    Factory function para obtener una instancia del servicio.
    
    Returns:
        Instancia de PokeneasService
    """
    return PokeneasService()
