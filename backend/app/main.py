import logging

from fastapi import FastAPI

from app.utils.logger import get_logger
from app.routers import (
    image
)

logger = get_logger(__name__)

app = FastAPI()

for router in [
    image.router
]:
    app.include_router(router)

@app.get("/")
def read_root():
    logger.info("Hello World")
    return {"message": "Hello World"}

