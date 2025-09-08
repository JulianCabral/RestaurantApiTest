import pytest

def pytest_addoption(parser):
    """Esta función registra el argumento de línea de comandos --api-url."""
    parser.addoption(
        "--api-url", 
        action="store", 
        default="http://127.0.0.1:8000", 
        help="URL base de la API a probar"
    )

@pytest.fixture
def base_url(pytestconfig):
    """Esta fixture lee el valor de --api-url y lo hace disponible para las pruebas."""
    # Se usa guion bajo (_) para leer la opción
    return pytestconfig.getoption("api_url")