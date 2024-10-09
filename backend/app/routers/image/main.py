from fastapi import APIRouter
from app.core.image.Emotion import Emotion


router = APIRouter(prefix="/image", tags=["image"], responses={404: {"description": "Not found"}})

@router.get("/")
def read_root():
    return {"message": "from image router"}

