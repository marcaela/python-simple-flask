import sys
sys.path.insert(0, '.')

import os
from flask import Flask, jsonify
from app import rate_limit, rate_limit_store
import time

def test_custom_rate_limit_via_env():
    """Test that rate_limit decorator respects provided max_requests and window."""
    # Create a fresh test app to avoid interfering with other tests
    test_app = Flask(__name__)
    test_store = {}
    
    # Custom rate limit parameters
    custom_max = 2
    custom_window = 60
    
    # Create a decorator instance with custom values
    limiter = rate_limit(max_requests=custom_max, window_seconds=custom_window)
    
    @test_app.route('/test-limit', methods=['POST'])
    @limiter
    def test_endpoint():
        return jsonify(success=True), 200
    
    client = test_app.test_client()
    
    # Make allowed number of requests
    for i in range(custom_max):
        response = client.post('/test-limit', json={"test": i})
        assert response.status_code == 200, f"Request {i} should be allowed"
    
    # Next request should be rate limited
    response = client.post('/test-limit', json={"test": "extra"})
    assert response.status_code == 429
    data = response.get_json()
    assert data is not None
    assert data.get("error") == "Rate limit exceeded"
    
    print("test_custom_rate_limit_via_env PASSED")

if __name__ == '__main__':
    test_custom_rate_limit_via_env()
