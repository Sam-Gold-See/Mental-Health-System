from fastapi import APIRouter
from sqlmodel import select

from .models import User, UserCreate, UserPublic
from app.utils.logger import get_logger
from .controller import *
from app.db.main import SessionDB


logger = get_logger(__name__)

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


@router.get("/")
def get_users(sessionDB: SessionDB):
    users = sessionDB.exec(select(User)).all()
    return [UserPublic.model_validate(user) for user in users]


@router.post("/")
def create_user(user: UserCreate, sessionDB: SessionDB):
    db_user = User(name=user.name, email=user.email, phone=user.phone, password=user.password)
    sessionDB.add(db_user)
    sessionDB.commit()
    sessionDB.refresh(db_user)
    return UserPublic.model_validate(db_user)
