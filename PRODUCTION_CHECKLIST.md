# Production-Readiness Checklist & Automation Guide

## Production-Readiness Checklist

### Security

- [ ] Replace dummy user with real user management (database, hashed passwords)
- [ ] Use a strong, unique JWT secret key (never hardcoded)
- [ ] Restrict CORS `allowed_origins` to trusted domains only
- [ ] Enforce HTTPS (use a reverse proxy like Nginx with SSL)
- [ ] Store secrets in environment variables or a secrets manager
- [ ] Regularly rotate credentials and secrets

### Error Handling & Logging

- [ ] Add global exception handlers for common errors (validation, auth, etc.)
- [ ] Use structured logging (JSON logs, log rotation, etc.)
- [ ] Integrate with monitoring/alerting (e.g., Sentry, Prometheus)

### Dependency Management

- [ ] Pin all dependencies in `requirements.txt` or `pyproject.toml`
- [ ] Regularly update dependencies and check for vulnerabilities

### Testing

- [ ] Add unit and integration tests (e.g., with `pytest`)
- [ ] Mock AWS S3 in tests (e.g., with `moto`)
- [ ] Add test coverage reporting

### Deployment

- [ ] Use an ASGI server (e.g., `uvicorn`, `gunicorn`) for production
- [ ] Containerize the app with Docker
- [ ] Add health/readiness endpoints (e.g., `/health`)
- [ ] Set up CI/CD for automated deployment

### Documentation

- [ ] Add OpenAPI descriptions and examples to endpoints/models
- [ ] Write a clear README with setup, environment, and deployment instructions

### Performance & Scalability

- [ ] Reuse boto3 clients efficiently (avoid recreating per request)
- [x] Use async S3 libraries (`aioboto3`) for high concurrency (all S3 endpoints migrated to async)
- [ ] Load test the API under expected traffic

### Rate Limiting & Abuse Prevention

- [ ] Implement rate limiting (e.g., with `slowapi` or at the proxy level)
- [ ] Add audit logging for sensitive actions

---

## Automation Examples

### 1. Dependency Management

**CI Lint/Test with GitHub Actions:**

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pip install pytest flake8
      - run: flake8 .
      - run: pytest
```

### 2. Security

**Secrets Scanning:**

- Enable GitHub Advanced Security or use `truffleHog` in CI to scan for secrets.

**Environment Variables:**

- Use `.env` files for local, and set secrets in your CI/CD or container orchestrator.

### 3. Testing

**Test Automation with `pytest` and `moto`:**

```python
# tests/test_presigned.py
import boto3
from moto import mock_s3
from presigned import generate_presigned_get

@mock_s3
def test_generate_presigned_get():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")
    url = generate_presigned_get(s3, "test-bucket", "test-key")
    assert url.startswith("http")
```

### 4. Deployment

**Dockerfile:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Health Check Endpoint:**

```python
# In app.py
@app.get("/health")
def health():
    return {"status": "ok"}
```

### 5. Monitoring & Logging

**Sentry Integration:**

```python
import sentry_sdk
sentry_sdk.init(dsn="YOUR_SENTRY_DSN")
```

**Structured Logging:**

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
```

### 6. Rate Limiting

**slowapi Example:**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.get("/health")
@limiter.limit("5/minute")
def health():
    return {"status": "ok"}
```
