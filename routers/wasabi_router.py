from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from dependencies import get_wasabi_temp_creds


class WasabiTempCredsRequest(BaseModel):
    account: str = Field(..., description="Wasabi account ID, name, or alias.")
    username: str = Field(..., description="Username within the account.")
    password: str = Field(..., description="Password for the user.")
    mfa_token: Optional[str] = Field(None, description="MFA token if required.")
    expires: Optional[int] = Field(
        None, description="Expiration in seconds (max 129600)."
    )
    security_token: Optional[str] = Field(None, description="Optional security token.")


router = APIRouter(prefix="/wasabi", tags=["wasabi"])


@router.post("/temp-credentials", summary="Get Wasabi Temporary Access Credentials")
async def create_temp_creds(payload: WasabiTempCredsRequest):
    """
    Obtain temporary Wasabi access credentials using the CreateTemporaryAccessCredentials action.
    """
    try:
        creds = await get_wasabi_temp_creds(
            account=payload.account,
            username=payload.username,
            password=payload.password,
            mfa_token=payload.mfa_token,
            expires=payload.expires,
            security_token=payload.security_token,
        )
        return creds
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to get Wasabi temporary credentials: {str(e)}",
        )
