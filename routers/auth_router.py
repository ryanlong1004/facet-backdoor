"""Auth endpoints router."""

import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/token", tags=["auth"])


class S3SessionLoginRequest(BaseModel):
    aws_access_key_id: str = Field(..., description="AWS/Wasabi access key")
    aws_secret_access_key: str = Field(..., description="AWS/Wasabi secret key")
    region_name: str = Field(..., description="AWS region name")
    endpoint_url: str = Field(..., description="S3 endpoint URL (e.g., Wasabi)")


@router.post("/login", response_model=dict)
async def login(payload: S3SessionLoginRequest) -> dict:
    """
    Accept S3 session parameters and return them directly. No authentication or token is issued.
    """
    logging.info("Authorization removed: returning S3 session parameters directly.")
    return {
        "aws_access_key_id": payload.aws_access_key_id,
        "aws_secret_access_key": payload.aws_secret_access_key,
        "region_name": payload.region_name,
        "endpoint_url": payload.endpoint_url,
    }
