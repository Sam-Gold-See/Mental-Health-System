from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .models import UserCreate, UserLogin, UserPublic, pwd_context
from pydantic import UUID4, BaseModel
from .repository import (
    get_user_from_db,
    create_user_in_db,
    get_user_from_db_by_email_or_phone,
)
from app.utils.logger import get_logger
from .controller import *
from app.db.main import get_session
from app.dependencies import get_current_user, token_manager

logger = get_logger(__name__)


router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


@router.get("/me")
def get_user(
    user_id: UUID4 = Depends(get_current_user),
    sessionDB: Session = Depends(get_session),
) -> UserPublic:
    user = get_user_from_db(user_id, sessionDB)
    return UserPublic.model_validate(user)


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserPublic


@router.post("/login")
def 登录(user: UserLogin, sessionDB: Session = Depends(get_session)) -> LoginResponse:
    db_user = get_user_from_db_by_email_or_phone(user.type, user.login_info, sessionDB)
    if not db_user:
        raise HTTPException(status_code=401, detail="用户不存在")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="密码错误")
    return {
        "access_token": token_manager.create_access_token(db_user.user_id),
        "refresh_token": token_manager.create_refresh_token(db_user.user_id),
        "user": UserPublic.model_validate(db_user),
    }


class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserPublic


@router.post("/register")
def 注册(
    user: UserCreate, sessionDB: Session = Depends(get_session)
) -> RegisterResponse:
    db_user = create_user_in_db(user, sessionDB)
    return {
        "access_token": token_manager.create_access_token(db_user.user_id),
        "refresh_token": token_manager.create_refresh_token(db_user.user_id),
        "user": UserPublic.model_validate(db_user),
    }
