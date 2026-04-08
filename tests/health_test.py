import pytest
from app import app

def test_health_endpoint():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'version' in data


def test_version_endpoint():
    client = app.test_client()
    response = client.get('/version')
    assert response.status_code == 200
    data = response.get_json()
    assert 'version' in data
    assert data['version'] == "1.0.0"


def test_echo_endpoint():
    client = app.test_client()
    response = client.post('/echo', json={'message': 'hello'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'hello'


def test_echo_empty():
    client = app.test_client()
    response = client.post('/echo', content_type='application/json')
    # Without body, returns empty dict (or 400 depending on Flask version)
    assert response.status_code in (200, 400)
