from app.routers.users.models import User, UserCreate
from sqlmodel import select, Session
from pydantic import UUID4, EmailStr
from typing import Literal


def get_user_from_db(user_id: UUID4, sessionDB: Session) -> User | None:
    user = sessionDB.exec(select(User).where(User.user_id == user_id)).first()
    return user


def get_user_from_db_by_email_or_phone(
    type: Literal["email", "phone"], login_info: EmailStr | str, sessionDB: Session
) -> User | None:
    if type == "email":
        user = sessionDB.exec(select(User).where(User.email == login_info)).first()
    else:
        user = sessionDB.exec(select(User).where(User.phone == login_info)).first()
    return user


def create_user_in_db(user: UserCreate, sessionDB: Session) -> User:
    db_user = User(
        name=user.name, email=user.email, phone=user.phone, password=user.password
    )
    sessionDB.add(db_user)
    sessionDB.commit()
    sessionDB.refresh(db_user)
    return db_user
