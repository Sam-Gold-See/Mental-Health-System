from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

from app.config import SQL_URL

connect_args = {"check_same_thread": False}
engine = create_engine(SQL_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

SessionDB = Annotated[Session, Depends(get_session)]