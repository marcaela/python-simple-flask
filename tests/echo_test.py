import pytest
from app import app

def test_echo_endpoint():
    client = app.test_client()
    response = client.post('/echo', json={"message": "hello"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "hello"
    assert "request_id" in data

def test_echo_endpoint_empty():
    client = app.test_client()
    response = client.post('/echo')
    assert response.status_code == 400

def test_echo_endpoint_invalid_json():
    client = app.test_client()
    response = client.post('/echo', data="not json", content_type='text/plain')
    assert response.status_code == 400