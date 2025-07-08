"""Main FastAPI app with routers and dependency injection."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from config import settings
# Routers
from routers.auth_router import router as auth_router
from routers.presigned_router import router as presigned_router
from routers.s3_router import router as s3_router

app = FastAPI(
    title="Facet Backdoor API",
    description="API for authentication, S3 presigned URLs, and bucket operations.",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "Authentication and AWS token endpoints."},
        {
            "name": "presigned",
            "description": "Endpoints for generating S3 presigned URLs.",
        },
        {"name": "s3", "description": "Endpoints for S3 bucket operations."},
    ],
)


# Custom error handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": True, "status_code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "error": True,
            "status_code": 422,
        },
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


# Register routers
app.include_router(auth_router)
app.include_router(presigned_router)
app.include_router(s3_router)


# Healthcheck endpoint
@app.get("/healthz", tags=["health"])
async def healthcheck():
    """Healthcheck endpoint for readiness/liveness probes."""
    return {"status": "ok"}
