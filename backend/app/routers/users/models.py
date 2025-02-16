from typing import Literal
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator, UUID4
import datetime
import uuid
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: EmailStr | None = Field(unique=True, index=True, default=None)
    phone: str | None = Field(default=None)


class User(UserBase, table=True):
    __tablename__ = "users"
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
        return pwd_context.hash(password)

class UserLogin(SQLModel):
    type: Literal["email", "phone"]
    login_info: EmailStr | str
    password: str

class UserPublic(UserBase):
    user_id: UUID4
