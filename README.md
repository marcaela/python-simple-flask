# Simple Flask App

A minimal Flask application exposing health, version, status, and echo endpoints.

## Usage

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

| Endpoint   | Method | Description                     |
|------------|--------|---------------------------------|
| `/`        | GET    | Returns "Hello, World!"        |
| `/health`  | GET    | Returns status, version, timestamp |
| `/ready`  | GET    | Returns readiness status |
| `/version` | GET    | Returns API version             |
| `/status`  | GET    | Returns request details         |
| `/echo`    | POST   | Echoes back JSON payload        |
| `/ping`    | GET    | Returns "Pong!"                 |
| `/headers` | GET    | Returns request headers (debugging) |
| `/time`    | GET    | Returns current UTC time        |

## Testing

```bash
pytest tests/
```

## Version

Defined in `config.py`.