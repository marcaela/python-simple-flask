import pytest
from app import app

def test_health_endpoint():
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'app' in data
    assert data['app'] == 'python-simple-flask'
    assert 'version' in data
    assert 'timestamp' in data


def test_status_endpoint():
    client = app.test_client()
    response = client.get('/status')
    assert response.status_code == 200
    data = response.get_json()
    assert 'version' in data
    assert 'endpoint' in data
    assert data['endpoint'] == '/status'
    assert 'method' in data
    assert 'timestamp' in data


def test_version_endpoint():
    client = app.test_client()
    response = client.get('/version')
    assert response.status_code == 200
    data = response.get_json()
    assert 'version' in data
    assert data['version'] == "v0.2.1"
    assert 'app' in data


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


def test_request_id_generated():
    client = app.test_client()
    response = client.get('/version')
    assert response.status_code == 200
    # Request ID should be generated automatically
    data = response.get_json()
    # version endpoint doesn't include request_id, but next requests should have it
    response2 = client.get('/status')
    data2 = response2.get_json()
    assert 'request_id' in data2
