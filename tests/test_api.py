"""
Tests para los endpoints de la API.
"""
import json


class TestPokeneaAPI:
    """Tests para el endpoint /api/pokenea"""
    
    def test_api_pokenea_returns_200(self, client):
        """Verifica que el endpoint retorna 200."""
        response = client.get('/api/pokenea')
        assert response.status_code == 200
    
    def test_api_pokenea_returns_json(self, client):
        """Verifica que el endpoint retorna JSON."""
        response = client.get('/api/pokenea')
        assert response.content_type == 'application/json'
    
    def test_api_pokenea_has_required_fields(self, client):
        """Verifica que el JSON tiene los campos requeridos."""
        response = client.get('/api/pokenea')
        data = json.loads(response.data)
        
        required_fields = ['id', 'nombre', 'altura', 'habilidad', 'container_id']
        for field in required_fields:
            assert field in data, f"Campo '{field}' no encontrado en la respuesta"
    
    def test_api_pokenea_field_types(self, client):
        """Verifica los tipos de datos de los campos."""
        response = client.get('/api/pokenea')
        data = json.loads(response.data)
        
        assert isinstance(data['id'], int), "id debe ser un entero"
        assert isinstance(data['nombre'], str), "nombre debe ser un string"
        assert isinstance(data['altura'], str), "altura debe ser un string"
        assert isinstance(data['habilidad'], str), "habilidad debe ser un string"
        assert isinstance(data['container_id'], str), "container_id debe ser un string"
    
    def test_api_pokenea_container_id_present(self, client):
        """Verifica que container_id no esté vacío."""
        response = client.get('/api/pokenea')
        data = json.loads(response.data)
        
        assert data['container_id'], "container_id no debe estar vacío"
        assert len(data['container_id']) > 0, "container_id debe tener contenido"
    
    def test_api_pokenea_valid_id_range(self, client):
        """Verifica que el ID esté en el rango válido (1-10)."""
        response = client.get('/api/pokenea')
        data = json.loads(response.data)
        
        assert 1 <= data['id'] <= 10, "ID debe estar entre 1 y 10"
    
    def test_api_pokenea_randomness(self, client):
        """Verifica que el endpoint retorna diferentes Pokeneas (probabilísticamente)."""
        ids = set()
        # Hacer múltiples requests para verificar aleatoriedad
        for _ in range(20):
            response = client.get('/api/pokenea')
            data = json.loads(response.data)
            ids.add(data['id'])
        
        # Con 20 requests de 10 posibles, deberíamos ver al menos 3 diferentes
        assert len(ids) >= 3, "El endpoint debería retornar diferentes Pokeneas"


class TestPokeneaView:
    """Tests para la vista /pokenea"""
    
    def test_pokenea_view_returns_200(self, client):
        """Verifica que la vista retorna 200."""
        response = client.get('/pokenea')
        assert response.status_code == 200
    
    def test_pokenea_view_returns_html(self, client):
        """Verifica que la vista retorna HTML."""
        response = client.get('/pokenea')
        assert 'text/html' in response.content_type
    
    def test_pokenea_view_contains_container_id(self, client):
        """Verifica que la vista contiene el container_id."""
        response = client.get('/pokenea')
        html = response.data.decode('utf-8')
        
        # Buscar el badge del container
        assert '🐳' in html or 'container' in html.lower()
    
    def test_pokenea_view_contains_quote(self, client):
        """Verifica que la vista contiene una frase filosófica."""
        response = client.get('/pokenea')
        html = response.data.decode('utf-8')
        
        # La frase está en un blockquote
        assert '<blockquote>' in html or 'frase' in html.lower()
    
    def test_pokenea_view_has_image_or_placeholder(self, client):
        """Verifica que la vista tiene imagen o placeholder."""
        response = client.get('/pokenea')
        html = response.data.decode('utf-8')
        
        # Debe tener imagen o placeholder
        assert '<img' in html or 'placeholder' in html.lower() or 'no disponible' in html.lower()


class TestHealthEndpoint:
    """Tests para el endpoint de health check."""
    
    def test_health_endpoint_returns_200(self, client):
        """Verifica que el health check retorna 200."""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self, client):
        """Verifica que el health check retorna JSON."""
        response = client.get('/health')
        assert response.content_type == 'application/json'
    
    def test_health_endpoint_status(self, client):
        """Verifica que el health check indica estado saludable."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestIndexRoute:
    """Tests para la ruta raíz."""
    
    def test_index_returns_200(self, client):
        """Verifica que la ruta raíz retorna 200."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_returns_html(self, client):
        """Verifica que la ruta raíz retorna HTML."""
        response = client.get('/')
        assert 'text/html' in response.content_type
