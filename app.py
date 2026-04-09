from flask import Flask, jsonify, request
from config import VERSION
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/version')
def version():
    return jsonify(version=VERSION)

@app.route('/health')
def health():
    return jsonify(status='ok', version=VERSION)

@app.route('/echo', methods=['POST'])
def echo():
    try:
        data = request.get_json()
        if data is None:
            return jsonify(error="Invalid JSON"), 400
        return jsonify(data)
    except Exception as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run()