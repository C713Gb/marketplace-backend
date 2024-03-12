from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product():
    response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "A test product", "price": 10.99, "seller_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert "id" in data

def test_get_product():
    # Assuming you have a product with ID 1
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
