import requests
import pytest
from uuid import uuid4

# --- Fixtures de Pytest (Ayudantes para las pruebas) ---

@pytest.fixture
def new_dish_payload():
    """Proporciona un payload base para crear un nuevo plato con un nombre único."""
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
    assert response.status_code == 201, "Fallo en la creación del plato para la prueba."
    return response.json()

@pytest.fixture
def another_created_dish(new_dish_payload, base_url):
    """Crea un segundo plato para pruebas de conflictos y filtros."""
    payload = new_dish_payload
    payload["name"] = f"Pasta Test {uuid4()}" # Nombre diferente para evitar conflicto inicial
    payload["category"] = 2 # Categoría diferente
    payload["price"] = 12.50
    response = requests.post(f"{base_url}/api/v1/Dish", json=payload)
    assert response.status_code == 201, "Fallo en la creación del segundo plato para la prueba."
    return response.json()

# --- Pruebas para POST /api/v1/Dish ---

def test_post_create_dish_success(new_dish_payload, base_url):
    """✅ Valida la creación exitosa de un plato (Status 201)."""
    response = requests.post(f"{base_url}/api/v1/Dish", json=new_dish_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_dish_payload["name"]
    assert "id" in data

def test_post_create_dish_duplicate_name_fails(created_dish, base_url):
    """❌ Valida que no se pueda crear un plato con un nombre repetido (Status 409)."""
    duplicate_payload = {
        "name": created_dish["name"], # Usando el nombre del plato ya creado
        "description": "Otro plato con el mismo nombre.",
        "price": 10.00,
        "category": 1,
    }
    response = requests.post(f"{base_url}/api/v1/Dish", json=duplicate_payload)
    assert response.status_code == 409

@pytest.mark.parametrize("invalid_price", [0, -10.50])
def test_post_create_dish_invalid_price_fails(new_dish_payload, base_url, invalid_price):
    """❌ Valida que un precio de cero o negativo falle (Status 400)."""
    new_dish_payload["price"] = invalid_price
    response = requests.post(f"{base_url}/api/v1/Dish", json=new_dish_payload)
    assert response.status_code == 400

@pytest.mark.parametrize("missing_field", ["name", "price", "category"])
def test_post_create_dish_missing_required_field_fails(new_dish_payload, base_url, missing_field):
    """❌ Valida que la falta de un campo obligatorio falle (Status 400)."""
    del new_dish_payload[missing_field]
    response = requests.post(f"{base_url}/api/v1/Dish", json=new_dish_payload)
    assert response.status_code == 400

# --- Pruebas para GET /api/v1/Dish ---

def test_get_all_dishes(base_url):
    """✅ Valida la obtención de la lista de platos (Status 200)."""
    response = requests.get(f"{base_url}/api/v1/Dish")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_filter_by_name(created_dish, base_url):
    """✅ Valida el filtrado por nombre."""
    dish_name = created_dish["name"]
    response = requests.get(f"{base_url}/api/v1/Dish", params={"name": dish_name})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(dish["name"] == dish_name for dish in data)

def test_get_filter_by_category(created_dish, another_created_dish, base_url):
    """✅ Valida el filtrado por categoría."""
    category_id = created_dish["category"]["id"]
    response = requests.get(f"{base_url}/api/v1/Dish", params={"category": category_id})
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(dish["category"]["id"] == category_id for dish in data)

@pytest.mark.parametrize("sort_order, is_reversed", [("asc", False), ("desc", True)])
def test_get_sort_by_price(base_url, sort_order, is_reversed):
    """✅ Valida el ordenamiento por precio ascendente y descendente."""
    response = requests.get(f"{base_url}/api/v1/Dish", params={"sortByPrice": sort_order})
    assert response.status_code == 200
    dishes = response.json()
    if len(dishes) > 1:
        prices = [dish["price"] for dish in dishes]
        assert prices == sorted(prices, reverse=is_reversed)

# --- Pruebas para PUT /api/v1/Dish/{id} ---

def test_put_update_dish_success(created_dish, base_url):
    """✅ Valida la actualización exitosa de un plato (Status 200)."""
    dish_id = created_dish["id"]
    update_payload = {
        "name": "Pizza Súper Actualizada",
        "description": "Descripción totalmente nueva.",
        "price": 99.99,
        "category": 1,
        "image": "http://example.com/new_image.jpg",
        "isActive": False
    }
    response = requests.put(f"{base_url}/api/v1/Dish/{dish_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pizza Súper Actualizada"
    assert data["price"] == 99.99
    assert data["isActive"] is False

def test_put_update_nonexistent_dish_fails(base_url):
    """❌ Valida que actualizar un plato inexistente falle (Status 404)."""
    non_existent_id = str(uuid4())
    update_payload = {"name": "Inexistente", "price": 10.00, "category": 1, "isActive": True}
    response = requests.put(f"{base_url}/api/v1/Dish/{non_existent_id}", json=update_payload)
    assert response.status_code == 404

def test_put_update_dish_with_conflicting_name_fails(created_dish, another_created_dish, base_url):
    """❌ Valida que no se pueda actualizar un plato con el nombre de otro ya existente (Status 409)."""
    id_to_update = created_dish["id"]
    conflicting_name = another_created_dish["name"] # Nombre del OTRO plato
    
    update_payload = {
        "name": conflicting_name,
        "description": "Intentando causar un conflicto.",
        "price": 1.00,
        "category": 1,
        "isActive": True
    }
    response = requests.put(f"{base_url}/api/v1/Dish/{id_to_update}", json=update_payload)
    assert response.status_code == 409