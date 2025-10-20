"""
Blueprint de Pokeneas - Rutas principales de la aplicación.
"""
from flask import Blueprint, jsonify, render_template, render_template_string, current_app
import boto3
import os
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


@pokeneas_bp.route('/imagenes', methods=['GET'])
def mostrar_imagenes():
    """
    Endpoint que muestra todas las imágenes almacenadas en S3.
    
    Retorna una página HTML con todas las imágenes del bucket S3.
    """
    try:
        # Obtener credenciales de S3 desde la configuración
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY'),
            region_name=current_app.config.get('S3_REGION', 'us-east-1')
        )
        
        S3_BUCKET = current_app.config.get('S3_BUCKET')
        
        if not S3_BUCKET:
            return render_template_string(
                "<h1>Error</h1><p>Bucket S3 no configurado</p>"
            ), 500
        
        # Obtener la lista de objetos (archivos) del bucket
        objects = s3.list_objects_v2(Bucket=S3_BUCKET)
        
        # Extraer los nombres de los archivos y construir URLs
        image_urls = []
        for obj in objects.get("Contents", []):
            key = obj["Key"]
            url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
            image_urls.append(url)
        
        # Renderizar una plantilla HTML básica con las imágenes
        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Imágenes desde S3</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                .image-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 20px;
                    margin-top: 30px;
                }
                .image-card {
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .image-card img {
                    width: 100%;
                    height: auto;
                    border-radius: 4px;
                }
                .image-card small {
                    display: block;
                    margin-top: 10px;
                    color: #666;
                    word-break: break-all;
                }
            </style>
        </head>
        <body>
            <h1>🖼️ Imágenes desde S3</h1>
            <div class="image-grid">
            {% for url in image_urls %}
                <div class="image-card">
                    <img src="{{ url }}" alt="Imagen S3">
                    <small>{{ url }}</small>
                </div>
            {% endfor %}
            </div>
        </body>
        </html>
        """
        return render_template_string(html, image_urls=image_urls)
        
    except Exception as e:
        current_app.logger.error(f"Error en /imagenes: {e}")
        return render_template_string(
            f"<h1>Error</h1><p>Error al obtener imágenes: {str(e)}</p>"
        ), 500
