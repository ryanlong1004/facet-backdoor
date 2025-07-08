"""Authentication logic and dependencies."""

import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import settings

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dummy user for demonstration (in production, use a database)
fake_user = {
    "username": "testuser",
    "hashed_password": pwd_context.hash("testpass"),
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    result = pwd_context.verify(plain_password, hashed_password)
    logging.info("Password verification attempted.")
    return result


def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user by username and password."""
    is_authenticated = username == fake_user["username"] and verify_password(
        password, fake_user["hashed_password"]
    )
    logging.info(
        "Authentication attempt for user '%s': %s.",
        username,
        "success" if is_authenticated else "failure",
    )
    return is_authenticated


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    import datetime as dt

    to_encode = data.copy()
    expire = dt.datetime.now(dt.UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.algorithm)
    logging.info("Access token created for user: %s", data.get("sub"))
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Dependency to get the current user from a JWT token."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        username = payload.get("sub")
        if username is None:
            logging.warning("JWT decode failed: no subject in token.")
            raise credentials_exception
        username_str: str = str(username)
    except JWTError as exc:
        logging.warning("JWT decode error: %s", exc)
        raise credentials_exception from exc
    if username_str != fake_user["username"]:
        logging.warning("Token user '%s' does not match fake user.", username_str)
        raise credentials_exception
    logging.info("Token validated for user: %s", username_str)
    return username_str
