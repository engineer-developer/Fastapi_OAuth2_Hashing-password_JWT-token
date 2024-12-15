from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.utils import authenticate_user, create_access_token
from config.config import settings
from database.database import CommonAsyncScopedSession
from dto.tokens.schemas import Token

router = APIRouter(tags=["Auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: CommonAsyncScopedSession,
):
    """
    Get credentials from form-data and create access_token.
    In this case uses "Content-type": "application/x-www-form-urlencoded"
    """
    incorrect_credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect username or password",
    )

    email = form_data.username
    password = form_data.password

    user = await authenticate_user(session, email, password)
    if not user:
        raise incorrect_credentials_exception

    access_token_expires = timedelta(
        minutes=settings.auth.access_token_expire_minutes,
    )
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
