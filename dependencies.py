from typing import Any, AsyncGenerator

import aioboto3

from config import settings


async def get_async_s3_client(
    endpoint_url: str,
    aws_access_key_id: str,
    aws_secret_access_key: str,
    region_name: str,
) -> AsyncGenerator[Any, None]:
    """
    Async dependency to provide a configured aioboto3 S3 client.
    All connection parameters must be passed explicitly.
    """
    session = aioboto3.Session()
    try:
        s3_client_cm = session.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
    except Exception:
        import logging
        logging.exception("Failed to create aioboto3 S3 client")
        raise
    s3_client = await s3_client_cm.__aenter__()
    try:
        yield s3_client
    finally:
        await s3_client_cm.__aexit__(None, None, None)
