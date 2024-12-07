from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_password_hash
from src.dao.models import Password
from src.dto.passwords.schemas import PasswordCreateSchema


async def create_password_instance(
    password: str,
) -> Password:
    """Create instance of Password"""

    hashed_password = await get_password_hash(password)

    new_password_schema = PasswordCreateSchema(
        hashed_password=hashed_password,
    )
    return Password(**new_password_schema.model_dump())
