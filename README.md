# Facet Backdoor API

[![CI/CD Pipeline](https://github.com/ryanlong1004/facet-backdoor/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/ryanlong1004/facet-backdoor/actions/workflows/ci-cd.yml)

## Overview

Facet Backdoor API is a FastAPI-based service for authentication, S3-compatible storage operations, and presigned URL generation. It supports both AWS S3 and Wasabi, with async endpoints for high concurrency.

---

## Features

- **Authentication**: JWT-based login endpoint (`/token/login`).
- **Presigned URLs**: Generate presigned GET/PUT/POST/DELETE URLs for S3 objects (`/presigned/*`).
- **Bucket Operations**: List objects in S3 buckets (`/bucket/list`).
- **Wasabi Temporary Credentials**: Obtain temporary Wasabi credentials (`/wasabi/temp-credentials`).
- **Async S3**: All S3 operations use `aioboto3` for async performance.
- **CORS**: Configurable allowed origins.
- **Healthcheck**: `/healthz` endpoint for readiness/liveness probes.

---

## Setup

1. **Clone the repo**
2. **Install dependencies**
   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configure environment**
   - Copy `.env.example` to `.env` and fill in your secrets and config.
   - Key variables: `VITE_ACCESS_KEY`, `VITE_SECRET_KEY`, `VITE_BUCKET_NAME`, etc.
4. **Run the app**
   ```sh
   uvicorn app:app --reload
   ```

---

## Docker

Build and run with Docker:

```sh
docker build -t facet-backdoor:local .
docker run --rm -p 9650:9650 --env-file .env facet-backdoor:local
```

---

## API Endpoints

### Auth

- `POST /token/login` — Get JWT access token

### Presigned URLs

- `POST /presigned/get` — Get presigned GET URL
- `POST /presigned/put` — Get presigned PUT URL
- `POST /presigned/post` — Get presigned POST URL
- `POST /presigned/delete` — Get presigned DELETE URL

### S3 Buckets

- `GET /bucket/list` — List objects in a bucket

### Wasabi

- `POST /wasabi/temp-credentials` — Get temporary Wasabi credentials

### Health

- `GET /healthz` — Healthcheck endpoint

---

## Testing

- Run all tests: `pytest`
- Example test: see `tests/test_app.py`

---

## Configuration

- All config is via `.env` and/or environment variables. See `.env.example` for options.
- Uses Pydantic `BaseSettings` for type safety.

---

## Production

- Use the provided `Dockerfile` for production builds.
- Run behind a reverse proxy (e.g., Nginx) for HTTPS.
- See `PRODUCTION_CHECKLIST.md` for hardening and deployment tips.

---

## Notes

- Wasabi does **not** support AWS STS `get_session_token`. Use `/wasabi/temp-credentials` for temporary keys.
- All S3 endpoints are async for high concurrency.
- CORS is restricted by default; configure as needed in `.env`.
