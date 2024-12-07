from typing import Annotated, Optional, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.auth.utils import (
    get_current_active_admin,
    get_current_active_user,
    get_current_user,
)
from src.dao.models import Password, User
from src.database.database import CommonAsyncSession
from src.dto.passwords.utils import create_password_instance
from src.dto.users.schemas import (
    DeleteConfirmSchema,
    ErrorDetailSchema,
    UserCreateSchema,
    UserOutSchema,
    UserUpdateSchema,
)
from src.dto.users.utils import fetch_all_users, fetch_user_by_id

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Users not found",
)


@router.get("/me", response_model=UserOutSchema)
async def get_profile_of_logging_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get logging user"""

    return current_user


@router.get(
    "",
    dependencies=[Depends(get_current_active_user)],
    response_model=list[UserOutSchema],
    responses={
        404: {
            "description": "Users not found",
            "model": ErrorDetailSchema,
        },
    },
)
async def get_all_users(
    session: CommonAsyncSession,
) -> Sequence[User]:
    """Get all users from database"""

    users_orm = await fetch_all_users(session)
    if not users_orm:
        raise user_not_found_exception
    return users_orm


@router.get(
    "/{user_id}",
    dependencies=[Depends(get_current_active_user)],
    response_model=UserOutSchema,
)
async def get_user_by_id(
    session: CommonAsyncSession,
    user_id: int,
) -> Optional[User]:
    """Get user by id from database"""

    user = await fetch_user_by_id(session, user_id)
    if not user:
        raise user_not_found_exception
    return user


@router.post(
    "",
    dependencies=[Depends(get_current_active_admin)],
    response_model=UserOutSchema,
    status_code=201,
    responses={
        409: {
            "description": "Error: Conflict",
            "model": ErrorDetailSchema,
        },
    },
)
async def add_new_user(
    session: CommonAsyncSession,
    user: UserCreateSchema,
) -> Optional[User]:
    """Add new user to database"""

    try:
        async with session.begin():
            new_password_orm: Password = await create_password_instance(
                user.password,
            )
            session.add(new_password_orm)
            await session.flush()
            new_user_orm = User(**user.model_dump(exclude={"password"}))
            new_user_orm.password_id = new_password_orm.id
            session.add(new_user_orm)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{
                exc.orig.args.__str__().rsplit(sep=":")[-1].strip(".',) ")
                if exc.orig
                else exc.__repr__()
            }",
        )
    return new_user_orm


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_admin)],
    response_model=UserOutSchema,
)
async def update_partial_user(
    session: CommonAsyncSession,
    user_id: int,
    updated_user: UserUpdateSchema,
) -> Optional[User]:
    """Update user partially"""

    user = await fetch_user_by_id(session, user_id)
    if not user:
        raise user_not_found_exception

    for name, value in updated_user.model_dump(exclude_unset=True).items():
        setattr(user, name, value)
    await session.commit()
    return user


@router.delete(
    "/{user_id}",
    dependencies=[Depends(get_current_active_admin)],
    response_model=DeleteConfirmSchema,
)
async def delete_user(
    session: CommonAsyncSession,
    user_id: int,
) -> dict[str, str]:
    """Delete user from database"""

    user = await fetch_user_by_id(session, user_id)
    if not user:
        raise user_not_found_exception
    await session.delete(user)
    await session.commit()
    return {"deleted": "True"}
