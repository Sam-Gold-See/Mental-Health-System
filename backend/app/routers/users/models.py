from typing import Literal
from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.orm import declarative_mixin
from pydantic import BaseModel, EmailStr, field_validator, UUID4
import datetime
import uuid
from passlib.context import CryptContext
from app.db.main import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@declarative_mixin
class UserBase:
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)


class User(Base, UserBase):
    __tablename__ = "users"
    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    password = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
    )


class UserCreate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    password: str

    @field_validator("phone")
    def validate_contact(cls, phone: str | None, info) -> str | None:
        email = info.data.get("email")
        if not phone and not email:
            raise ValueError("邮箱和手机号至少需要填写一个")
        return phone

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        return pwd_context.hash(password)
