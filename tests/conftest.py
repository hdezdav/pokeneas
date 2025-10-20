"""
Configuración de pytest.
"""
import pytest
from app import create_app


@pytest.fixture
def app():
    """Fixture de la aplicación Flask en modo testing."""
    app = create_app('testing')
    yield app


@pytest.fixture
def client(app):
    """Fixture del cliente de prueba."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture del CLI runner."""
    return app.test_cli_runner()
