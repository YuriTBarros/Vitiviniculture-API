"""
Authentication route: receives username and password, validates credentials,
and returns a JWT token if successful.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from api.core.security import verify_password, create_access_token,hash_password
from api.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

#Temporary in-memory user store for testing
hashed = hash_password("secret123")
fake_users_db = {
    "yuri": {
        "username": "yuri",
        "hashed_password": hashed
    }
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    POST /auth/login
    Authenticates user and returns a JWT access token.

    Body (x-www-form-urlencoded):
    - username: str
    - password: str

    Response:
    - access_token: str
    - token_type: "bearer"
    """

    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}