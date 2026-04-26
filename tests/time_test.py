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

def test_time_endpoint_with_offset():
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

def test_time_endpoint_with_utc_offset():
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
    assert data['timezone'] == 'UTC'

def test_time_endpoint_with_offset():
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
    assert data['timezone'] == 'UTC'