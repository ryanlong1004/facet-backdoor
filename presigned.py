"""
Presigned S3 URL generation utilities for FastAPI endpoints.
All functions raise HTTPException on error and log the exception.
"""

import logging

from fastapi import HTTPException


async def async_generate_presigned_get(
    s3_client, bucket_name, object_key, expiration=3600
):
    """Async: Generate a presigned GET URL for an S3 object."""
    try:
        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
    except Exception as exc:
        logging.exception("Failed to generate presigned GET URL")
        raise HTTPException(
            status_code=500, detail="Failed to generate presigned GET URL."
        ) from exc


async def async_generate_presigned_put(
    s3_client, bucket_name, object_key, expiration=3600
):
    """Async: Generate a presigned PUT URL for an S3 object."""
    try:
        return s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
    except Exception as exc:
        logging.exception("Failed to generate presigned PUT URL")
        raise HTTPException(
            status_code=500, detail="Failed to generate presigned PUT URL."
        ) from exc


async def async_generate_presigned_post(
    s3_client, bucket_name, object_key, expiration=3600
):
    """Async: Generate a presigned POST policy for an S3 object."""
    try:
        return s3_client.generate_presigned_post(
            Bucket=bucket_name,
            Key=object_key,
            ExpiresIn=expiration,
        )
    except Exception as exc:
        logging.exception("Failed to generate presigned POST data")
        raise HTTPException(
            status_code=500, detail="Failed to generate presigned POST data."
        ) from exc


async def async_generate_presigned_delete(
    s3_client, bucket_name, object_key, expiration=3600
):
    """Async: Generate a presigned DELETE URL for an S3 object."""
    try:
        return s3_client.generate_presigned_url(
            "delete_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
    except Exception as exc:
        logging.exception("Failed to generate presigned DELETE URL")
        raise HTTPException(
            status_code=500, detail="Failed to generate presigned DELETE URL."
        ) from exc
