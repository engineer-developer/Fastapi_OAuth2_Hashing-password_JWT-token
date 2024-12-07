import hashlib
import uuid
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import oauth2_scheme
from src.dao.models import User
from src.database.database import CommonAsyncScopedSession
from src.dto.users.utils import fetch_user_by_email


async def make_hashed_password(
    password: str,
    salt: str | None = None,
) -> tuple[str, str]:
    """Make hashed password from given password"""

    if not salt:
        salt = uuid.uuid4().hex
    mix = (password + salt).encode()
    hashed_password = hashlib.sha512(mix).hexdigest()
    return hashed_password, salt


async def is_correct_password(
    hashed_pw: str,
    salt: str,
    password: str,
) -> bool:
    """Check equality given password with hashed password"""

    result = await make_hashed_password(password, salt)
    return hashed_pw == result[0]


async def create_token() -> str:
    """Create token for tracking user registration"""

    some_token = ""
    return some_token


async def get_current_user(
    session: CommonAsyncScopedSession,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Optional[User]:
    """Get current login user"""

    user = await fetch_user_by_email(session, token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> Optional[User]:
    """Get current active login user"""

    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
