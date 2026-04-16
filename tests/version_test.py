import sys
sys.path.insert(0, '/home/runner/.openclaw/workspace')
from app import app

def test_version():
    client = app.test_client()
    response = client.get('/version')
    assert response.status_code == 200
    assert b'"version"' in response.data

def test_version_format():
    client = app.test_client()
    response = client.get('/version')
    assert b'v0' in response.data