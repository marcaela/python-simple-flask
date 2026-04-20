import app as application


def test_headers_returns_dict():
    client = application.app.test_client()
    response = client.get('/headers')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)