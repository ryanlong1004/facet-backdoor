"""
Configuration management for environment variables and settings.
Uses Pydantic BaseSettings for type safety and .env support.
"""

import os
from typing import List

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables from .env file before any settings are used
load_dotenv()


class Settings(BaseSettings):
    vite_auth0_domain: str = Field(
        default_factory=lambda: os.getenv("VITE_AUTH0_DOMAIN", "")
    )
    vite_auth0_client_id: str = Field(
        default_factory=lambda: os.getenv("VITE_AUTH0_CLIENT_ID", "")
    )
    vite_customer_id: str = Field(
        default_factory=lambda: os.getenv("VITE_CUSTOMER_ID", "")
    )
    vite_access_key: str = Field(
        default_factory=lambda: os.getenv("VITE_ACCESS_KEY", "")
    )
    vite_secret_key: str = Field(
        default_factory=lambda: os.getenv("VITE_SECRET_KEY", "")
    )
    vite_bucket_region: str = Field(
        default_factory=lambda: os.getenv("VITE_BUCKET_REGION", "")
    )
    vite_bucket_name: str = Field(
        default_factory=lambda: os.getenv("VITE_BUCKET_NAME", "")
    )
    vite_bucket_endpoint: str = Field(
        default_factory=lambda: os.getenv("VITE_BUCKET_ENDPOINT", "")
    )
    vite_api_base_url: str = Field(
        default_factory=lambda: os.getenv("VITE_API_BASE_URL", "")
    )
    vite_cache_ttl: str = Field(default_factory=lambda: os.getenv("VITE_CACHE_TTL", ""))
    vite_cache_max: str = Field(default_factory=lambda: os.getenv("VITE_CACHE_MAX", ""))
    vite_person_faces_cache_key: str = Field(
        default_factory=lambda: os.getenv("VITE_PERSON_FACES_CACHE_KEY", "")
    )
    vite_pagination_limit: str = Field(
        default_factory=lambda: os.getenv("VITE_PAGINATION_LIMIT", "")
    )
    vite_disable_person_faces_cache: str = Field(
        default_factory=lambda: os.getenv("VITE_DISABLE_PERSON_FACES_CACHE", "")
    )
    jwt_secret_key: str = Field(
        default_factory=lambda: os.getenv("JWT_SECRET_KEY", "change_this_secret")
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    wasabi_endpoint: str = Field(
        default_factory=lambda: os.getenv(
            "WASABI_ENDPOINT", "https://s3.us-east-1.wasabisys.com"
        )
    )
    aws_region: str = Field(
        default_factory=lambda: os.getenv("AWS_REGION", "us-east-1")
    )
    allowed_origins: List[str] = Field(
        default_factory=lambda: os.getenv("ALLOWED_ORIGINS", "*").split(",")
    )

    model_config = {"env_file": ".env"}


settings = Settings()
