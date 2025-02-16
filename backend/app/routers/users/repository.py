from app.routers.users.models import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import UUID4, EmailStr
from typing import Literal


async def get_user_from_db(user_id: UUID4, sessionDB: AsyncSession) -> User | None:
    result = await sessionDB.execute(select(User).where(User.user_id == user_id))
    return result.scalar_one_or_none()


async def get_user_from_db_by_email_or_phone(
    type: Literal["email", "phone"], login_info: EmailStr | str, sessionDB: AsyncSession
) -> User | None:
    if type == "email":
        result = await sessionDB.execute(select(User).where(User.email == login_info))
    else:
        result = await sessionDB.execute(select(User).where(User.phone == login_info))
    return result.scalar_one_or_none()


async def create_user_in_db(user: UserCreate, sessionDB: AsyncSession) -> User:
    db_user = User(
        name=user.name, email=user.email, phone=user.phone, password=user.password
    )
    sessionDB.add(db_user)
    await sessionDB.commit()
    await sessionDB.refresh(db_user)
    return db_user
