"""
Blueprint de Pokeneas - Rutas principales de la aplicación.
"""
from flask import Blueprint, jsonify, render_template, current_app
from app.services.pokeneas_service import get_pokeneas_service

# Crear blueprint
pokeneas_bp = Blueprint('pokeneas', __name__)


@pokeneas_bp.route('/api/pokenea', methods=['GET'])
def get_pokenea_api():
    """
    Endpoint API que retorna un Pokenea aleatorio en formato JSON.
    
    Returns:
        JSON con: id, nombre, altura, habilidad, container_id
    """
    try:
        service = get_pokeneas_service()
        pokenea_data = service.get_pokenea_for_api()
        return jsonify(pokenea_data), 200
    except Exception as e:
        current_app.logger.error(f"Error en /api/pokenea: {e}")
        return jsonify({
            "error": "Error al obtener Pokenea",
            "message": str(e)
        }), 500


@pokeneas_bp.route('/pokenea', methods=['GET'])
def get_pokenea_view():
    """
    Endpoint que renderiza la vista HTML con un Pokenea aleatorio.
    
    Muestra: imagen, frase filosófica y container_id
    """
    try:
        service = get_pokeneas_service()
        pokenea_data = service.get_pokenea_for_view()
        return render_template('pokenea.html', pokenea=pokenea_data), 200
    except Exception as e:
        current_app.logger.error(f"Error en /pokenea: {e}")
        return render_template(
            'error.html',
            error_message="Error al cargar el Pokenea"
        ), 500


@pokeneas_bp.route('/', methods=['GET'])
def index():
    """Ruta principal que redirige a la vista de Pokenea."""
    return get_pokenea_view()
