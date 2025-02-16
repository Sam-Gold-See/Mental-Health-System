from sqlmodel import create_engine, SQLModel, Session

from app.config import config

connect_args = {"check_same_thread": False}
engine = create_engine(config.DB_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
