import logging
from flask import Flask, jsonify, request
from datetime import datetime, timezone, timedelta
from config import APP_NAME, VERSION
import uuid

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.before_request
def add_request_id():
    request.id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])

@app.after_request
def log_request(response):
    logger.info(f"{request.method} {request.path} - {response.status_code} - {request.id}")
    return response

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/version')
def version():
    return jsonify(version=VERSION)

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

if __name__ == '__main__':
    app.run()