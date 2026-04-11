# Simple Flask App

A minimal Flask application exposing health, version, status, and echo endpoints.

A minimal Flask application with a health check endpoint.

## Usage

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

- `GET /` - Returns "Hello, World!"
- `GET /health` - Returns JSON with status and version

## Version

Defined in `config.py`.
