import pytest
from app import app

def test_ping_endpoint():
    client = app.test_client()
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data == b"Pong!"