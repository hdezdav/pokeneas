"""
Configuración de la aplicación Flask por entornos.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Config:
    """Configuración base."""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # AWS S3
    S3_BUCKET = os.getenv('S3_BUCKET', '')
    S3_REGION = os.getenv('S3_REGION', 'us-east-1')
    S3_PUBLIC_BASE_URL = os.getenv('S3_PUBLIC_BASE_URL', '')
    USE_S3_PRESIGNED = os.getenv('USE_S3_PRESIGNED', 'false').lower() == 'true'
    
    # AWS Credentials
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN', '')
    
    # Presigned URL Configuration
    PRESIGNED_URL_EXPIRATION = int(os.getenv('PRESIGNED_URL_EXPIRATION', '3600'))
    
    @staticmethod
    def init_app(app):
        """Inicialización específica de configuración."""
        pass


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    TESTING = False
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        # Configuración adicional para producción
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug:
            file_handler = RotatingFileHandler(
                'logs/pokeneas.log',
                maxBytes=10240,
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Pokeneas startup')


class TestingConfig(Config):
    """Configuración para testing."""
    TESTING = True
    DEBUG = True
    # Usar bucket de prueba o mock
    S3_BUCKET = 'test-bucket'
    USE_S3_PRESIGNED = False


# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Obtiene la configuración según el entorno."""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
