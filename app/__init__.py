"""
Application Factory para Flask.
"""
import os
from flask import Flask
from app.config import get_config


def create_app(config_name=None):
    """
    Crea y configura la aplicación Flask.
    
    Args:
        config_name: Nombre de la configuración a usar (development, production, testing)
    
    Returns:
        Aplicación Flask configurada
    """
    # Configurar rutas de templates y static desde la raíz del proyecto
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, 
                template_folder=template_dir,
                static_folder=static_dir)
    
    # Cargar configuración
    if config_name:
        from app.config import config
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)
    else:
        config_class = get_config()
        app.config.from_object(config_class)
        config_class.init_app(app)
    
    # Registrar blueprints
    from app.blueprints.pokeneas import pokeneas_bp
    app.register_blueprint(pokeneas_bp)
    
    # Ruta de salud para verificar que la app está corriendo
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app
