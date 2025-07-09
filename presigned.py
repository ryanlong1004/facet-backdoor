"""
Presigned S3 URL generation utilities for FastAPI endpoints.
All functions raise HTTPException on error and log the exception.
"""

import logging

from fastapi import HTTPException


def extract_s3_credentials(headers):
    """
    Extract S3/Wasabi credentials from request headers.
    Returns a dict with keys: aws_access_key_id, aws_secret_access_key, aws_session_token (optional).
    Raises HTTPException(400) if required headers are missing.
    """
    required_headers = [
        "x-aws-access-key-id",
        "x-aws-secret-access-key",
    ]
    creds = {}
    for h in required_headers:
        v = headers.get(h)
        if not v:
            logging.error("Missing required header: %s", h)
            raise HTTPException(
                status_code=400,
                detail=f"Missing required header: {h}",
            )
        logging.info("Extracted header %s: %s... (redacted)", h, v[:4])
        creds[h.replace("x-aws-", "aws_").replace("-", "_")] = v
    # Session token is now required for all requests
    session_token = headers.get("x-aws-session-token")
    if session_token is None or session_token == "":
        logging.error("Missing required header: x-aws-session-token")
        raise HTTPException(
            status_code=400,
            detail="Missing required header: x-aws-session-token",
        )
    logging.info("Extracted session token: %s... (redacted)", session_token[:4])
    creds["aws_session_token"] = session_token
    return creds


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
