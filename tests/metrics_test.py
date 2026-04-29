import sys
sys.path.insert(0, '.')
from app import app

def test_metrics_endpoint():
    client = app.test_client()
    response = client.get('/metrics')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_requests' in data
    assert 'requests_by_method' in data
    assert 'requests_by_endpoint' in data
    assert 'avg_response_time_ms' in data
    assert 'p50_response_time_ms' in data
    assert 'p95_response_time_ms' in data
    assert 'p99_response_time_ms' in data
    assert 'uptime_since' in data
    assert 'uptime_seconds' in data
    print("test_metrics_endpoint PASSED")

if __name__ == '__main__':
    test_metrics_endpoint()