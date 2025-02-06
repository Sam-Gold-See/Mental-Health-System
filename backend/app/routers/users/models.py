from pydantic import field_validator
from sqlmodel import SQLModel, Field
import datetime
import uuid


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: str = Field(
        default_factory = lambda: str(uuid.uuid4()),
        primary_key     = True,
        index           = True,
        description     = "用户ID",
    )
    name    : str = Field(default="", description="用户名")
    email   : str = Field(default="", description="邮箱")
    phone   : str = Field(default="", description="手机号")
    password: str = Field(default="", description="密码")

    created_at: datetime.datetime = Field(
        default_factory = lambda: datetime.datetime.now(datetime.timezone.utc),
        description     = "创建时间",
    )
    updated_at: datetime.datetime = Field(
        default_factory = lambda: datetime.datetime.now(datetime.timezone.utc),
        description     = "更新时间",
    )


class UserCreate(SQLModel):
    name: str
    email: str | None = Field(default=None, description="邮箱")
    phone: str | None = Field(default=None, description="手机号")
    password: str

    @field_validator("phone")
    def validate_contact(cls, phone: str | None, info) -> str | None:
        email = info.data.get("email")
        if not phone and not email:
            raise ValueError("邮箱和手机号至少需要填写一个")
        return phone


class UserPublic(SQLModel):
    user_id: str
    name   : str
    email  : str | None = None
    phone  : str | None = None
