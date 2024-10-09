from fastapi import FastAPI, APIRouter

from app.routers import (
    image
)

app = FastAPI()

for router in [
    image.router
]:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

