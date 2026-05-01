# Memory
- 2025-04-17: Added test for /status endpoint (test coverage)
- 2025-04-17: Improved README with endpoint table (docs improvement)
- 2025-04-20: Added /headers endpoint for debugging (feature)
- 2025-04-20: Added timezone offset support to /time endpoint (feature)
- 2025-04-21: Added `app` field to `/version` endpoint for consistency. Updated tests.
- 2025-04-23: Added offset tests for /time endpoint (test improvement)
- 2025-04-24: Added /headers endpoint to README docs table (doc improvement)
- 2025-04-27: Added uptime_seconds to /metrics endpoint (feature/test)
- 2026-04-27: Improved test coverage for /time endpoint (test improvement)
- 2026-04-26: Improved /time endpoint with better error handling for offset parameter (feature/test)
- 2026-04-27: Added uptime_seconds to /health endpoint and update test
Task completed: Added uptime_seconds to /health endpoint and updated corresponding test.
- 2026-04-28: refactor: extract time offset logic into utility function for /time endpoint
- 2026-04-28: refactor: extract uptime calculation into get_uptime_seconds() utility function
- 2026-04-29: feat: add percentile response times (p50, p95, p99) to /metrics endpoint
- 2026-04-29: test: add rate limit test for /echo endpoint
- 2026-04-30: feat: add min and max response times to metrics endpoint; fix tests
Task completed: Added response_time_sample_size to metrics endpoint.
- 2026-05-01: fix: use consistent time utility in health endpoint and add missing test importsTask completed: Made small improvements to health endpoint consistency and test imports.
