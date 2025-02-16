from fastapi import APIRouter, Depends
from sqlmodel import Session
from .models import UserCreate, UserPublic
from pydantic import UUID4
from .repository import get_user_from_db, create_user_in_db
from app.utils.logger import get_logger
from .controller import *
from app.db.main import get_session


logger = get_logger(__name__)

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)


@router.get("/")
def get_users(user_id: UUID4, sessionDB: Session = Depends(get_session)) -> list[UserPublic]:
    user = get_user_from_db(user_id, sessionDB)
    return UserPublic.model_validate(user)


@router.post("/")
def create_user(user: UserCreate, sessionDB: Session = Depends(get_session)) -> UserPublic:
    db_user = create_user_in_db(user, sessionDB)
    return UserPublic.model_validate(db_user)
