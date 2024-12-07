from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import make_hashed_password
from src.dao.models import Password
from src.dto.passwords.schemas import PasswordCreateSchema


async def create_password_instance(
    session: AsyncSession,
    password: str,
) -> Password:
    """Create instance of Password"""

    hashed_password, salt = await make_hashed_password(
        password=password,
    )

    new_password_schema = PasswordCreateSchema(
        hashed_password=hashed_password,
        salt=salt,
    )
    return Password(**new_password_schema.model_dump())
