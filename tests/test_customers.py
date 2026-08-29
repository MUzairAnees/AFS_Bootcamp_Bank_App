from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

BASE = "/api/v1/customers"


def test_create_customer_route_exists():
    response = client.post(BASE)
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: create customer"}


def test_list_customers_route_exists():
    response = client.get(BASE)
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: list customers"}


def test_get_customer_route_exists():
    response = client.get(f"{BASE}/97")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: get customer 97"}


def test_update_customer_route_exists():
    response = client.put(f"{BASE}/97")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: update customer 97"}


def test_delete_customer_route_exists():
    response = client.delete(f"{BASE}/97")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: deactivate customer 97"}


def test_customer_id_must_be_an_integer():
    response = client.get(f"{BASE}/not-a-number")
    assert response.status_code == 422
