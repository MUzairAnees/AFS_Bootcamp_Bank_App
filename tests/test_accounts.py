from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

BASE = "/api/v1/accounts"


def test_create_account_route_exists():
    response = client.post(BASE)
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: open account"}


def test_list_accounts_route_exists():
    response = client.get(BASE)
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: list accounts"}


def test_get_account_route_exists():
    response = client.get(f"{BASE}/1001")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: get account 1001"}


def test_delete_account_route_exists():
    response = client.delete(f"{BASE}/1001")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: deactivate account 1001"}


def test_account_number_must_be_an_integer():
    response = client.get(f"{BASE}/not-a-number")
    assert response.status_code == 422
