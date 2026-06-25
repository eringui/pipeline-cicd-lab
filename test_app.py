import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_retorna_200(client):
    res = client.get("/")
    assert res.status_code == 200

def test_index_retorna_status_ok(client):
    res = client.get("/")
    data = res.get_json()
    assert data["status"] == "ok"

def test_health_retorna_healthy(client):
    res = client.get("/health")
    data = res.get_json()
    assert data["status"] == "healthy"
    assert res.status_code == 200