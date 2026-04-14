# Memory

## 2025-04-14
- Added test for /ping endpoint (tests/ping_test.py), added pytest to requirements.txt, fixed version assertion in health_test.py to match actual v0.2.1

## 2025-04-10
- Added request ID tracking (uuid) with X-Request-ID header support, included in /status and /echo responses

## 2025-04-09
- Fixed /echo endpoint to handle invalid JSON and exceptions properly