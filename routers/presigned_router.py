"""Presigned S3 URL endpoints router."""

from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from auth import get_current_user
from dependencies import get_async_s3_client
from models import PresignRequest
from presigned import (
    async_generate_presigned_delete,
    async_generate_presigned_get,
    async_generate_presigned_post,
    async_generate_presigned_put,
)

router = APIRouter(prefix="/presigned", tags=["presigned"])


@router.post("/get", response_model=dict)
async def api_presigned_get(
    req: PresignRequest,
    _: str = Depends(get_current_user),
    s3_client: Any = Depends(get_async_s3_client),
) -> JSONResponse:
    """Generate a presigned GET URL for an S3 object (async)."""
    url = await async_generate_presigned_get(
        s3_client, req.bucket, req.key, req.expiration
    )
    return JSONResponse(content={"url": url})


@router.post("/put", response_model=dict)
async def api_presigned_put(
    req: PresignRequest,
    _: str = Depends(get_current_user),
    s3_client: Any = Depends(get_async_s3_client),
) -> JSONResponse:
    """Generate a presigned PUT URL for an S3 object (async)."""
    url = await async_generate_presigned_put(
        s3_client, req.bucket, req.key, req.expiration
    )
    return JSONResponse(content={"url": url})


@router.post("/post", response_model=dict)
async def api_presigned_post(
    req: PresignRequest,
    _: str = Depends(get_current_user),
    s3_client: Any = Depends(get_async_s3_client),
) -> JSONResponse:
    """Generate a presigned POST policy for an S3 object (async)."""
    post_data = await async_generate_presigned_post(
        s3_client, req.bucket, req.key, req.expiration
    )
    return JSONResponse(content=post_data)


@router.post("/delete", response_model=dict)
async def api_presigned_delete(
    req: PresignRequest,
    _: str = Depends(get_current_user),
    s3_client: Any = Depends(get_async_s3_client),
) -> JSONResponse:
    """Generate a presigned DELETE URL for an S3 object (async)."""
    url = await async_generate_presigned_delete(
        s3_client, req.bucket, req.key, req.expiration
    )
    return JSONResponse(content={"url": url})
