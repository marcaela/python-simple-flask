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
    return jsonify(request.get_json() or {})

if __name__ == '__main__':
    app.run()