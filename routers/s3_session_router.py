import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


class S3SessionRequest(BaseModel):
    aws_access_key_id: str = Field(..., description="AWS/Wasabi access key")
    aws_secret_access_key: str = Field(..., description="AWS/Wasabi secret key")
    region_name: str = Field(..., description="AWS region name")
    endpoint_url: str = Field(..., description="S3 endpoint URL (e.g., Wasabi)")


class S3SessionTestResponse(BaseModel):
    buckets: list[str]


router = APIRouter(prefix="/s3", tags=["s3"])


@router.post("/session-test", response_model=S3SessionTestResponse)
async def create_s3_session(payload: S3SessionRequest):
    """
    Create a boto3 S3 session with provided credentials and return a list of buckets (test connection).
    """
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=payload.aws_access_key_id,
            aws_secret_access_key=payload.aws_secret_access_key,
            region_name=payload.region_name,
            endpoint_url=payload.endpoint_url,
        )
        response = s3.list_buckets()
        buckets = [b["Name"] for b in response.get("Buckets", [])]
        return S3SessionTestResponse(buckets=buckets)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create S3 session or list buckets: {str(e)}",
        )
