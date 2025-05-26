from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_autocomplete_empty():
    """GET /api/v1/autocomplete?q= пустой запрос — пустой список."""
    response = client.get('/api/v1/autocomplete?q=')
    assert response.status_code == 200
    assert response.json() == []


def test_autocomplete_known_query():
    """GET /api/v1/autocomplete?q=Новос — список с Новосибирском."""
    response = client.get('/api/v1/autocomplete?q=Новос')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any('Новосибирск' in city for city in data)
