import sys
sys.path.insert(0, '.')

import pytest
from app import app, rate_limit_store

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

def test_echo_endpoint_rate_limit():
    # Clear the rate limit store before the test
    rate_limit_store.clear()
    client = app.test_client()
    # Make 5 requests (should be allowed)
    for i in range(5):
        response = client.post('/echo', json={"message": f"test{i}"})
        assert response.status_code == 200, f"Request {i} failed"
    # 6th request should be rate limited
    response = client.post('/echo', json={"message": "blocked"})
    assert response.status_code == 429
    assert response.get_json()["error"] == "Rate limit exceeded"