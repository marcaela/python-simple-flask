import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

def test_time_endpoint_with_offset_non_utc():
    client = app.test_client()
    # Test with positive offset and non-UTC tz
    response = client.get('/time?tz=TEST&offset=2')
    assert response.status_code == 200
    data = response.get_json()
    assert 'timezone' in data
    assert 'timestamp' in data
    assert data['timezone'] == 'TEST'

    # Test with negative offset
    response = client.get('/time?tz=TEST&offset=-5')
    assert response.status_code == 200
    data = response.get_json()
    assert 'timezone' in data
    assert 'timestamp' in data
    assert data['timezone'] == 'TEST'

def test_time_endpoint_with_offset_utc():
    client = app.test_client()
    # Test with positive offset
    response = client.get('/time?tz=UTC&offset=2')
    assert response.status_code == 200
    data = response.get_json()
    assert 'timezone' in data
    assert 'timestamp' in data
    assert data['timezone'] == 'UTC'

    # Test with negative offset
    response = client.get('/time?tz=UTC&offset=-5')
    assert response.status_code == 200
    data = response.get_json()
    assert 'timezone' in data
    assert 'timestamp' in data
    assert data['timezone'] == 'UTC'

def test_time_endpoint_with_offset_utc_at_boundary():
    client = app.test_client()
    # Test UTC with offset at max boundary
    response = client.get('/time?tz=UTC&offset=24')
    assert response.status_code == 200
    data = response.get_json()
    assert data['timezone'] == 'UTC'

    # Test UTC with offset at min boundary
    response = client.get('/time?tz=UTC&offset=-24')
    assert response.status_code == 200
    data = response.get_json()
    assert data['timezone'] == 'UTC'


def test_time_endpoint_with_offset_missing():
    client = app.test_client()
    # Test missing offset when tz is not UTC
    response = client.get('/time?tz=TEST')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Missing offset parameter'

def test_time_endpoint_with_offset_invalid():
    client = app.test_client()
    # Test invalid offset parameter
    response = client.get('/time?tz=TEST&offset=abc')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Invalid offset parameter'

def test_time_endpoint_with_offset_boundary_max():
    client = app.test_client()
    # Test exactly at max boundary (24)
    response = client.get('/time?tz=TEST&offset=24')
    assert response.status_code == 200
    data = response.get_json()
    assert 'timestamp' in data

def test_time_endpoint_with_offset_boundary_min():
    client = app.test_client()
    # Test exactly at min boundary (-24)
    response = client.get('/time?tz=TEST&offset=-24')
    assert response.status_code == 200
    data = response.get_json()
    assert 'timestamp' in data

def test_time_endpoint_with_offset_out_of_range_positive():
    client = app.test_client()
    # Test offset beyond max (25)
    response = client.get('/time?tz=TEST&offset=25')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'offset must be between -24 and 24 hours'

def test_time_endpoint_with_offset_out_of_range_negative():
    client = app.test_client()
    # Test offset beyond min (-25)
    response = client.get('/time?tz=TEST&offset=-25')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'offset must be between -24 and 24 hours'
