import pytest
from app import app

def test_time_endpoint():
    client = app.test_client()
    response = client.get('/time')
    assert response.status_code == 200
    data = response.get_json()
    assert 'timezone' in data
    assert 'timestamp' in data
    assert data['timezone'] == 'UTC'