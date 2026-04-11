from flask import Flask, jsonify, request
from datetime import datetime, timezone
from config import VERSION
import uuid
app = Flask(__name__)

@app.before_request
def add_request_id():
    request.id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/version')
def version():
    return jsonify(version=VERSION)

@app.route('/health')
def health():
    return jsonify(status='ok', version=VERSION, timestamp=datetime.now(timezone.utc).isoformat())

@app.route('/status')
def status():
    return jsonify(
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

@app.route('/ping')
def ping():
    return "Pong!", 200

if __name__ == '__main__':
    app.run()