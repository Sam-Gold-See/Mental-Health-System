from typing import Literal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4, BaseModel, EmailStr

from .models import UserCreate, pwd_context
from .repository import (
    get_user_from_db,
    create_user_in_db,
    get_user_from_db_by_email_or_phone,
)

from app.utils.logger import get_logger
from app.db.main import get_session
from app.dependencies import get_current_user, token_manager

logger = get_logger(__name__)


router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


class UserSelf(BaseModel):
    user_id: UUID4
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


@router.get("/me")
async def 我的(
    user_id: UUID4 = Depends(get_current_user),
    sessionDB: AsyncSession = Depends(get_session),
) -> UserSelf:
    user = await get_user_from_db(user_id, sessionDB)
    return user


class UserLoginRequest(BaseModel):
    type: Literal["email", "phone"]
    login_info: EmailStr | str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserSelf


@router.post("/login")
async def 登录(
    user: UserLoginRequest, sessionDB: AsyncSession = Depends(get_session)
) -> LoginResponse:
    db_user = await get_user_from_db_by_email_or_phone(
        user.type, user.login_info, sessionDB
    )
    if not db_user:
        raise HTTPException(status_code=401, detail="用户不存在")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="密码错误")
    return {
        "access_token": token_manager.create_access_token(db_user.user_id),
        "refresh_token": token_manager.create_refresh_token(db_user.user_id),
        "user": db_user,
    }


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserSelf


@router.post("/register")
async def 注册(
    user: UserCreate, sessionDB: AsyncSession = Depends(get_session)
) -> RegisterResponse:
    db_user = await create_user_in_db(user, sessionDB)
    return {
        "access_token": token_manager.create_access_token(db_user.user_id),
        "refresh_token": token_manager.create_refresh_token(db_user.user_id),
        "user": db_user,
    }


class UserPublicResponse(BaseModel):
    user_id: UUID4
    name: str


@router.get("/")
async def 获取用户(
    user_id: UUID4,
    sessionDB: AsyncSession = Depends(get_session),
) -> UserPublicResponse:
    user = await get_user_from_db(user_id, sessionDB)
    return user
