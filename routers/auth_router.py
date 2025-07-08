"""Auth endpoints router."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token
from config import settings

router = APIRouter(prefix="/token", tags=["auth"])


@router.post("/login", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    """Authenticate user and return JWT access token. Uses client_id and client_secret from settings."""
    client_id = getattr(settings, "vite_secret_key", None)
    client_secret = getattr(settings, "vite_access_key", None)
    if not client_id or not client_secret:
        logging.error("Server misconfiguration: client_id or client_secret missing.")
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: client_id or client_secret missing.",
        )
    if not authenticate_user(form_data.username, form_data.password):
        logging.warning("Failed login for user: %s", form_data.username)
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    logging.info("User %s authenticated successfully.", form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}
