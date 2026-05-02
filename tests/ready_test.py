import sys
sys.path.insert(0, '.')

from app import app, APP_NAME

def test_ready_endpoint():
    client = app.test_client()
    response = client.get('/ready')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ready'
    assert data['app'] == APP_NAME
    assert 'version' in data
    assert 'timestamp' in data

if __name__ == '__main__':
    test_ready_endpoint()
    print("test_ready_endpoint PASSED")
