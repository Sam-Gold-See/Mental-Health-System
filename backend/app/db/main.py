from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import config

Base = declarative_base()
connect_args = {"check_same_thread": False}

# 异步引擎
engine = create_async_engine(config.DB_URL, connect_args=connect_args)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
