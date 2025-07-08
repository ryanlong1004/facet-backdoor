from typing import Any, AsyncGenerator

import aioboto3

from config import settings


async def get_async_s3_client() -> AsyncGenerator[Any, None]:
    """Async dependency to provide a configured aioboto3 S3 client."""
    session = aioboto3.Session()
    try:
        s3_client_cm = session.client(
            "s3",
            endpoint_url=settings.wasabi_endpoint,
            aws_access_key_id=settings.vite_access_key,
            aws_secret_access_key=settings.vite_secret_key,
            region_name=settings.aws_region,
        )
    except Exception:
        # Log and raise for misconfiguration
        import logging

        logging.exception("Failed to create aioboto3 S3 client")
        raise
    s3_client = await s3_client_cm.__aenter__()
    try:
        yield s3_client
    finally:
        await s3_client_cm.__aexit__(None, None, None)
