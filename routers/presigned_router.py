"""Presigned S3 URL endpoints router."""

import logging

import boto3
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from models import PresignRequest
from presigned import (async_generate_presigned_delete,
                       async_generate_presigned_get,
                       async_generate_presigned_post,
                       async_generate_presigned_put, extract_s3_credentials)

router = APIRouter(prefix="/presigned", tags=["presigned"])


@router.post("/get", response_model=dict)
async def api_presigned_get(
    req: PresignRequest,
    request: Request,
) -> JSONResponse:
    """Generate a presigned GET URL for an S3 object (async)."""
    sensitive_headers = {
        "X-Wasabi-Access-Key-Id",
        "X-Wasabi-Secret-Access-Key",
        "X-Wasabi-Session-Token",
    }
    sanitized_headers = {
        k: (v if k not in sensitive_headers else "[REDACTED]")
        for k, v in request.headers.items()
    }
    logging.info(
        "Presigned GET: headers=%s, bucket=%s, key=%s, expiration=%s",
        sanitized_headers,
        req.bucket,
        req.key,
        req.expiration,
    )
    # Extract S3 credentials from headers using utility
    import boto3

    creds = extract_s3_credentials({k.lower(): v for k, v in request.headers.items()})
    region_name = request.headers.get("X-Region")
    endpoint_url = request.headers.get("X-Endpoint")
    if not all(
        [
            creds.get("aws_access_key_id"),
            creds.get("aws_secret_access_key"),
            region_name,
            endpoint_url,
        ]
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "Missing required Wasabi credential headers."},
        )
    client_kwargs = dict(
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    # Only add session token if present and non-empty
    session_token = creds.get("aws_session_token")
    logging.info("Session token used for signing: %r", session_token)
    if session_token is not None and session_token != "":
        client_kwargs["aws_session_token"] = session_token
    s3_client = boto3.client("s3", **client_kwargs)
    url = await async_generate_presigned_get(
        s3_client, req.bucket, req.key, req.expiration
    )
    logging.info(
        "Presigned GET URL generated: bucket=%s, key=%s, url=%s",
        req.bucket,
        req.key,
        url,
    )
    return JSONResponse(content={"url": url})


@router.post("/put", response_model=dict)
async def api_presigned_put(
    req: PresignRequest,
    request: Request,
) -> JSONResponse:
    """Generate a presigned PUT URL for an S3 object (async)."""
    logging.info(
        "Presigned PUT: headers=%s, bucket=%s, key=%s, expiration=%s",
        dict(request.headers),
        req.bucket,
        req.key,
        req.expiration,
    )
    import boto3

    creds = extract_s3_credentials({k.lower(): v for k, v in request.headers.items()})
    region_name = request.headers.get("X-Region")
    endpoint_url = request.headers.get("X-Endpoint")
    if not all(
        [
            creds.get("aws_access_key_id"),
            creds.get("aws_secret_access_key"),
            region_name,
            endpoint_url,
        ]
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "Missing required Wasabi credential headers."},
        )
    client_kwargs = dict(
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    session_token = creds.get("aws_session_token")
    logging.info("Session token used for signing: %r", session_token)
    if session_token is not None and session_token != "":
        client_kwargs["aws_session_token"] = session_token
    s3_client = boto3.client("s3", **client_kwargs)
    url = await async_generate_presigned_put(
        s3_client, req.bucket, req.key, req.expiration
    )
    logging.info(
        "Presigned PUT URL generated: bucket=%s, key=%s, url=%s",
        req.bucket,
        req.key,
        url,
    )
    return JSONResponse(content={"url": url})


@router.post("/post", response_model=dict)
async def api_presigned_post(
    req: PresignRequest,
    request: Request,
) -> JSONResponse:
    """Generate a presigned POST policy for an S3 object (async)."""
    logging.info(
        "Presigned POST: headers=%s, bucket=%s, key=%s, expiration=%s",
        dict(request.headers),
        req.bucket,
        req.key,
        req.expiration,
    )

    creds = extract_s3_credentials({k.lower(): v for k, v in request.headers.items()})
    region_name = request.headers.get("X-Region")
    endpoint_url = request.headers.get("X-Endpoint")
    if not all(
        [
            creds.get("aws_access_key_id"),
            creds.get("aws_secret_access_key"),
            region_name,
            endpoint_url,
        ]
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "Missing required Wasabi credential headers."},
        )
    client_kwargs = dict(
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    session_token = creds.get("aws_session_token")
    logging.info("Session token used for signing: %r", session_token)
    if session_token is not None and session_token != "":
        client_kwargs["aws_session_token"] = session_token
    s3_client = boto3.client("s3", **client_kwargs)
    post_data = await async_generate_presigned_post(
        s3_client, req.bucket, req.key, req.expiration
    )
    # Patch: ensure session token field is correct case for S3/Wasabi
    if "fields" in post_data and "x-amz-security-token" in post_data["fields"]:
        post_data["fields"]["X-Amz-Security-Token"] = post_data["fields"].pop(
            "x-amz-security-token"
        )
    logging.info(
        "Presigned POST policy generated: bucket=%s, key=%s, post_data_keys=%s",
        req.bucket,
        req.key,
        list(post_data.keys()),
    )
    return JSONResponse(content=post_data)


@router.post("/delete", response_model=dict)
async def api_presigned_delete(
    req: PresignRequest,
    request: Request,
) -> JSONResponse:
    """Generate a presigned DELETE URL for an S3 object (async)."""
    logging.info(
        "Presigned DELETE: headers=%s, bucket=%s, key=%s, expiration=%s",
        dict(request.headers),
        req.bucket,
        req.key,
        req.expiration,
    )
    import boto3

    creds = extract_s3_credentials({k.lower(): v for k, v in request.headers.items()})
    region_name = request.headers.get("X-Region")
    endpoint_url = request.headers.get("X-Endpoint")
    if not all(
        [
            creds.get("aws_access_key_id"),
            creds.get("aws_secret_access_key"),
            region_name,
            endpoint_url,
        ]
    ):
        return JSONResponse(
            status_code=400,
            content={"detail": "Missing required Wasabi credential headers."},
        )
    client_kwargs = dict(
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    session_token = creds.get("aws_session_token")
    logging.info("Session token used for signing: %r", session_token)
    if session_token is not None and session_token != "":
        client_kwargs["aws_session_token"] = session_token
    s3_client = boto3.client("s3", **client_kwargs)
    url = await async_generate_presigned_delete(
        s3_client, req.bucket, req.key, req.expiration
    )
    logging.info(
        "Presigned DELETE URL generated: bucket=%s, key=%s, url=%s",
        req.bucket,
        req.key,
        url,
    )
    return JSONResponse(content={"url": url})
