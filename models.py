"""Pydantic models for requests and responses."""

from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    """Request model for temporary AWS credentials."""

    duration: int = Field(
        3600,
        ge=900,
        le=43200,
        description="Session duration in seconds (15 min to 12 hours)",
    )


class PresignRequest(BaseModel):
    """Request model for S3 presigned URL generation."""

    bucket: str = Field(..., min_length=3, max_length=63, description="S3 bucket name")
    key: str = Field(..., min_length=1, max_length=1024, description="S3 object key")
    expiration: int = Field(
        3600, ge=60, le=86400, description="Expiration in seconds (1 min to 24 hours)"
    )

    @classmethod
    def validate_bucket(cls, value: str) -> str:
        """Validate bucket name against S3 naming rules."""
        import re

        pattern = r"^[a-z0-9.-]+$"
        if not re.match(pattern, value):
            raise ValueError("Bucket name must match pattern: ^[a-z0-9.-]+$")
        return value
