from flask import Flask, jsonify
from config import VERSION
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/health')
def health():
    return jsonify(status='ok', version=VERSION)

if __name__ == '__main__':
    app.run()