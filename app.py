"""Main FastAPI app with routers and dependency injection."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
