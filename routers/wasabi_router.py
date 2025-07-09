from typing import Optional

import boto3
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


class WasabiSTSRequest(BaseModel):
    access_key: str = Field(..., description="Wasabi access key")
    secret_key: str = Field(..., description="Wasabi secret key")
    duration_seconds: int = Field(
        3600,
        ge=900,
        le=129600,
        description="Session duration in seconds (15 min to 36 hours)",
    )
    region: str = Field("us-east-1", description="Region name")
    endpoint_url: str = Field(
        "https://sts.wasabisys.com", description="Wasabi STS endpoint URL"
    )


class WasabiSTSCredentials(BaseModel):
    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: str


router = APIRouter(prefix="/wasabi", tags=["wasabi"])


@router.post("/sts-session", response_model=WasabiSTSCredentials)
async def get_wasabi_sts_session(payload: WasabiSTSRequest):
    """
    Obtain temporary session credentials from Wasabi STS using direct credentials.
    """
    try:
        sts_client = boto3.client(
            "sts",
            aws_access_key_id=payload.access_key,
            aws_secret_access_key=payload.secret_key,
            region_name=payload.region,
            endpoint_url=payload.endpoint_url,
        )
        response = sts_client.get_session_token(
            DurationSeconds=payload.duration_seconds
        )
        credentials = response["Credentials"]
        return WasabiSTSCredentials(
            access_key_id=credentials["AccessKeyId"],
            secret_access_key=credentials["SecretAccessKey"],
            session_token=credentials["SessionToken"],
            expiration=str(credentials["Expiration"]),
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to get Wasabi STS session: {str(e)}"
        )
