"""Presigned S3 URL endpoints router."""

import logging

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from models import PresignRequest
from presigned import (async_generate_presigned_delete,
                       async_generate_presigned_get,
                       async_generate_presigned_post,
                       async_generate_presigned_put)

router = APIRouter(prefix="/presigned", tags=["presigned"])


@router.post("/get", response_model=dict)
async def api_presigned_get(
    req: PresignRequest,
    request: Request,
) -> JSONResponse:
    """Generate a presigned GET URL for an S3 object (async)."""
    sensitive_headers = {"X-Wasabi-Access-Key-Id", "X-Wasabi-Secret-Access-Key", "X-Wasabi-Session-Token"}
    sanitized_headers = {
        k: (v if k not in sensitive_headers else "[REDACTED]") for k, v in request.headers.items()
    }
    logging.info(
        "Presigned GET: headers=%s, bucket=%s, key=%s, expiration=%s",
        sanitized_headers,
        req.bucket,
        req.key,
        req.expiration,
    )
    # Extract and validate S3 credentials from headers
    try:
        client_kwargs = extract_s3_credentials(request.headers)
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    import boto3

    client_kwargs = dict(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    if session_token:
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
    aws_access_key_id = request.headers.get("X-Wasabi-Access-Key-Id")
    aws_secret_access_key = request.headers.get("X-Wasabi-Secret-Access-Key")
    region_name = request.headers.get("X-Region")
    endpoint_url = request.headers.get("X-Endpoint")
    session_token = request.headers.get("X-Wasabi-Session-Token")
    if not all([aws_access_key_id, aws_secret_access_key, region_name, endpoint_url]):
        return JSONResponse(
            status_code=400,
            content={"detail": "Missing required Wasabi credential headers."},
        )
    import boto3

    client_kwargs = dict(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    if session_token:
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
    aws_access_key_id = request.headers.get("X-Wasabi-Access-Key-Id")
    aws_secret_access_key = request.headers.get("X-Wasabi-Secret-Access-Key")
    region_name = request.headers.get("X-Region")
    endpoint_url = request.headers.get("X-Endpoint")
    session_token = request.headers.get("X-Wasabi-Session-Token")
    if not all([aws_access_key_id, aws_secret_access_key, region_name, endpoint_url]):
        return JSONResponse(
            status_code=400,
            content={"detail": "Missing required Wasabi credential headers."},
        )
    import boto3

    client_kwargs = dict(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    if session_token:
        client_kwargs["aws_session_token"] = session_token
    s3_client = boto3.client("s3", **client_kwargs)
    post_data = await async_generate_presigned_post(
        s3_client, req.bucket, req.key, req.expiration
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
    aws_access_key_id = request.headers.get("X-Wasabi-Access-Key-Id")
    aws_secret_access_key = request.headers.get("X-Wasabi-Secret-Access-Key")
    region_name = request.headers.get("X-Region")
    endpoint_url = request.headers.get("X-Endpoint")
    session_token = request.headers.get("X-Wasabi-Session-Token")
    if not all([aws_access_key_id, aws_secret_access_key, region_name, endpoint_url]):
        return JSONResponse(
            status_code=400,
            content={"detail": "Missing required Wasabi credential headers."},
        )
    import boto3

    client_kwargs = dict(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    if session_token:
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
