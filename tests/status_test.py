import pytest
from app import app

def test_status_endpoint():
    client = app.test_client()
    response = client.get('/status')
    assert response.status_code == 200
    data = response.get_json()
    assert 'request_id' in data
    assert 'version' in data
    assert 'endpoint' in data
    assert data['endpoint'] == '/status'