import urllib.parse
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_form_empty_cookie():
    """GET / без cookie — форма с пустым городом."""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Введите город' in response.text
    assert 'value=""' in response.text


def test_get_form_with_cookie():
    """GET / с cookie last_city — поле с городом."""
    city_encoded = urllib.parse.quote('Новосибирск')
    response = client.get('/', cookies={'last_city': city_encoded})
    assert response.status_code == 200
    assert 'value="Новосибирск"' in response.text
