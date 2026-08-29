from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

BASE = "/api/v1/branches"


def test_list_branches_route_exists():
    response = client.get(BASE)
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: list branches"}


def test_get_branch_route_exists():
    response = client.get(f"{BASE}/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: get branch 1"}


def test_transaction_volume_route_exists():
    response = client.get(f"{BASE}/1/transaction-volume")
    assert response.status_code == 200
    assert response.json() == {"detail": "TODO: transaction volume for branch 1"}


def test_branch_code_must_be_an_integer():
    response = client.get(f"{BASE}/not-a-number")
    assert response.status_code == 422
