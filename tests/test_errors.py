import pytest
from app import app

def test_404_endpoint():
    client = app.test_client()
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert data['error'] == 'Not found'

def test_405_endpoint():
    client = app.test_client()
    response = client.post('/ping')  # ping only accepts GET
    assert response.status_code == 405
    data = response.get_json()
    assert data['error'] == 'Method not allowed'