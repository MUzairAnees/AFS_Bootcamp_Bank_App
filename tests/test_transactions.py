from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

BASE = "/api/v1/transactions"


def test_deposit_route_exists():
    response = client.post(f"{BASE}/deposit")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: deposit"}


def test_withdraw_route_exists():
    response = client.post(f"{BASE}/withdraw")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: withdraw"}


def test_transfer_route_exists():
    response = client.post(f"{BASE}/transfer")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: transfer"}


def test_list_transactions_route_exists():
    response = client.get(BASE)
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: list transactions"}


def test_get_transaction_route_exists():
    response = client.get(f"{BASE}/5000000000")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: get transaction 5000000000"}


def test_transaction_id_must_be_an_integer():
    response = client.get(f"{BASE}/not-a-number")
    assert response.status_code == 422


def test_action_paths_do_not_collide_with_id_route():
    response = client.get(f"{BASE}/deposit")
    assert response.status_code == 422
