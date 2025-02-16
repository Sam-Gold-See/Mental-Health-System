from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator, UUID4
import datetime
import uuid
import bcrypt


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    phone: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID4 = Field(
        default_factory=lambda: uuid.uuid4(),
        primary_key=True,
        index=True,
        description="用户ID",
    )
    password: str

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        description="创建时间",
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        description="更新时间",
    )


class UserCreate(UserBase):
    password: str

    @field_validator("phone")
    def validate_contact(cls, phone: str | None, info) -> str | None:
        email = info.data.get("email")
        if not phone and not email:
            raise ValueError("邮箱和手机号至少需要填写一个")
        return phone

    # bcrypt 加密
    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


class UserPublic(UserBase):
    id: int
