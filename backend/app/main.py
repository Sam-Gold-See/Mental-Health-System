import os
from typing import Annotated

import dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.main import create_db_and_tables
from app.utils.logger import get_logger
from app.routers import (
    image,
    users
)

logger = get_logger(__name__)


# 生命周期
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 初始化数据库
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# 注册路由
for router in [
    image.router,
    users.router
]:
    app.include_router(router)


@app.get("/")
def read_root():
    logger.info("Hello World")
    return {"message": "Hello World"}

