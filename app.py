import logging
import time
from flask import Flask, jsonify, request
from datetime import datetime, timezone, timedelta
from config import APP_NAME, VERSION
import uuid
from functools import wraps

# Simple in-memory rate limiter
rate_limit_store = {}

def rate_limit(max_requests=10, window_seconds=60):
    """Simple rate limiting decorator."""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            client_ip = request.remote_addr
            key = f"{client_ip}:{request.endpoint}"
            now = time.time()
            
            if key not in rate_limit_store:
                rate_limit_store[key] = []
            
            # Clean old requests
            rate_limit_store[key] = [t for t in rate_limit_store[key] if now - t < window_seconds]
            
            if len(rate_limit_store[key]) >= max_requests:
                return jsonify(error="Rate limit exceeded"), 429
            
            rate_limit_store[key].append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Simple in-memory metrics
metrics = {
    'requests_total': 0,
    'requests_by_method': {},
    'requests_by_endpoint': {},
    'response_times': [],
    'start_time': datetime.now(timezone.utc).isoformat()
}

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.before_request
def add_request_id():
    request.id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])
    request.start_time = time.monotonic()
    metrics['requests_total'] += 1
    method = request.method
    metrics['requests_by_method'][method] = metrics['requests_by_method'].get(method, 0) + 1

@app.after_request
def log_request(response):
    duration = (time.monotonic() - request.start_time) * 1000
    metrics['response_times'].append(duration)
    if len(metrics['response_times']) > 1000:
        metrics['response_times'] = metrics['response_times'][-1000:]
    endpoint = request.path
    metrics['requests_by_endpoint'][endpoint] = metrics['requests_by_endpoint'].get(endpoint, 0) + 1
    logger.info(f"{request.method} {request.path} - {response.status_code} - {request.id} - {duration:.2f}ms")
    return response

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/version')
def version():
    return jsonify(app=APP_NAME, version=VERSION)

@app.route('/health')
def health():
    return jsonify(app=APP_NAME, status='ok', version=VERSION, timestamp=datetime.now(timezone.utc).isoformat())

@app.route('/status')
def status():
    return jsonify(
        app=APP_NAME,
        request_id=request.id,
        version=VERSION,
        endpoint=request.path,
        method=request.method,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@app.route('/echo', methods=['POST'])
@rate_limit(max_requests=5, window_seconds=60)
def echo():
    try:
        data = request.get_json()
        if data is None:
            return jsonify(error="Invalid JSON"), 400
        return jsonify(request_id=request.id, **data)
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/headers')
def headers():
    """Return request headers (useful for debugging)."""
    return jsonify(dict(request.headers))

@app.route('/ping')
def ping():
    return "Pong!", 200

@app.route('/time')
def get_time():
    """Return current server time in ISO format."""
    tz_name = request.args.get('tz', 'UTC')
    try:
        if tz_name != 'UTC':
            offset = int(request.args.get('offset', 0))
            td = timedelta(hours=offset)
            now = datetime.now(timezone.utc) + td
        else:
            now = datetime.now(timezone.utc)
        return jsonify(
            timezone=tz_name,
            timestamp=now.isoformat()
        )
    except ValueError:
        return jsonify(error="Invalid timezone parameter"), 400

@app.route('/metrics')
def get_metrics():
    """Return basic request metrics."""
    times = metrics['response_times']
    avg_time = sum(times) / len(times) if times else 0
    return jsonify(
        app=APP_NAME,
        total_requests=metrics['requests_total'],
        requests_by_method=metrics['requests_by_method'],
        requests_by_endpoint=metrics['requests_by_endpoint'],
        avg_response_time_ms=round(avg_time, 2),
        uptime_since=metrics['start_time']
    )

if __name__ == '__main__':
    app.run()