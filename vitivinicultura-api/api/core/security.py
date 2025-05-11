"""
Security utilities for password hashing, token generation, and user
    authentication.
---
Dependencies:
- passlib (bcrypt): For securely hashing and verifying passwords.
- python-jose: For creating and decoding JWT tokens.
- FastAPI OAuth2PasswordBearer: To extract tokens from requests and handle
    OAuth2 authentication.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from api.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt hashing algorithm.

    Arguments:
        password (str): The raw password input from the user.

    Returns:
        str: A securely hashed password that can be stored in a database.
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the given plaintext password matches the stored hashed
        password.

    Arguments:
        plain_password (str): The password provided by the user during login.
        hashed_password (str): The stored hashed password retrieved from the
            database.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a signed JWT access token with a specified expiration time.

    Arguments:
        data (dict): The data to be included in the token payload
            (e.g., {"sub": username}).
        expires_delta (Optional[timedelta]): The duration for which the token
            is valid. If None, defaults to a pre-configured expiration time.

    Returns:
        str: The signed JWT token as a string.
    """

    to_encode = data.copy()
    if isinstance(expires_delta, int):
        expires_delta = timedelta(minutes=expires_delta)
    elif expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )


class TokenData(BaseModel):
    """
    Model representing the payload of a JWT token.

    Attributes:
        username (Optional[str]): The username extracted from the
            JWT token ('sub' field).
    """

    username: Optional[str] = None


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extracts and validates the current user from the JWT token in the
        request header.

    Arguments:
        token (str): The JWT token extracted from the 'Authorization' header
            of the request.

    Returns:
        str: The username ('sub' field) of the user encoded in the JWT token.

    Raises:
        HTTPException: If the token is missing, expired, or invalid.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        return username
    except JWTError:
        raise credentials_exception
