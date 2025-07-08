"""S3 bucket listing endpoints router."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from auth import get_current_user
from config import settings
from dependencies import get_async_s3_client

router = APIRouter(prefix="/bucket", tags=["s3"])


@router.get("/list", response_model=dict)
async def list_bucket_objects(
    bucket: str = Query(
        default=None, description="Bucket name to list. Defaults to settings bucket."
    ),
    prefix: str = Query(default="", description="Prefix to filter objects."),
    s3_client: Any = Depends(get_async_s3_client),
    _: str = Depends(get_current_user),
) -> dict:
    """List all objects in the specified S3 bucket (async)."""
    if not bucket:
        bucket = getattr(settings, "vite_bucket_name", "")
        if not bucket:
            raise HTTPException(
                status_code=400,
                detail="Bucket name not specified in settings or request.",
            )
    try:
        paginator = s3_client.get_paginator("list_objects_v2")
        objects = []
        async for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                objects.append(
                    {
                        "key": obj["Key"],
                        "size": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat()
                        if hasattr(obj["LastModified"], "isoformat")
                        else str(obj["LastModified"]),
                    }
                )
        return {"objects": objects}
    except Exception as exc:
        logging.exception("Failed to list bucket objects")
        raise HTTPException(
            status_code=500, detail="Failed to list bucket objects."
        ) from exc
