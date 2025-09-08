import requests
import pytest
from uuid import uuid4

# --- Fixtures de Pytest para la configuración de datos de prueba ---

@pytest.fixture
def new_dish_payload():
    """Proporciona un payload de datos para crear un nuevo plato con un nombre único."""
    return {
        "name": f"Pizza Test {uuid4()}",
        "description": "Una deliciosa pizza para pruebas.",
        "price": 15.99,
        "category": 1, # Asume que la categoría con ID 1 ya existe
        "image": "http://example.com/image.jpg"
    }

@pytest.fixture
def created_dish(new_dish_payload, base_url):
    """Crea un plato nuevo antes de una prueba y devuelve sus datos."""
    response = requests.post(f"{base_url}/api/v1/Dish", json=new_dish_payload)
    assert response.status_code == 201
    return response.json()

# --- Pruebas para los endpoints ---

def test_create_dish_success(new_dish_payload, base_url):
    """Verifica que se pueda crear un plato correctamente."""
    response = requests.post(f"{base_url}/api/v1/Dish", json=new_dish_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_dish_payload["name"]
    assert "id" in data

def test_create_dish_duplicate_name_fails(created_dish, base_url):
    """Verifica que la API devuelva un error 409 al intentar crear un plato con un nombre repetido."""
    duplicate_payload = {
        "name": created_dish["name"],
        "description": "Otro plato con el mismo nombre.",
        "price": 10.00,
        "category": 1,
    }
    response = requests.post(f"{base_url}/api/v1/Dish", json=duplicate_payload)
    assert response.status_code == 409

def test_get_all_dishes(base_url):
    """Verifica que se pueda obtener una lista de platos."""
    response = requests.get(f"{base_url}/api/v1/Dish")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_dish_success(created_dish, base_url):
    """Verifica que se pueda actualizar un plato existente."""
    dish_id = created_dish["id"]
    update_payload = {
        "name": "Pizza Actualizada",
        "description": "Descripción actualizada.",
        "price": 25.50,
        "category": 1,
        "image": "http://example.com/new_image.jpg",
        "isActive": True
    }
    response = requests.put(f"{base_url}/api/v1/Dish/{dish_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pizza Actualizada"
    assert data["price"] == 25.50

def test_update_nonexistent_dish_fails(base_url):
    """Verifica que la API devuelva un error 404 al intentar actualizar un plato que no existe."""
    non_existent_id = str(uuid4())
    update_payload = {
        "name": "No importa el nombre",
        "price": 10.00,
        "category": 1,
        "isActive": True
    }
    response = requests.put(f"{base_url}/api/v1/Dish/{non_existent_id}", json=update_payload)
    assert response.status_code == 404