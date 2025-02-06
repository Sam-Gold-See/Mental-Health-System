import asyncio
import base64
import io

from fastapi import APIRouter, WebSocket
from PIL import Image

from app.utils.logger import get_logger
from .controller import ImageController
from concurrent.futures import ThreadPoolExecutor

logger = get_logger(__name__)

executor = ThreadPoolExecutor(max_workers=1)

router = APIRouter(prefix="/image", tags=["image"], responses={404: {"description": "Not found"}})

@router.websocket("/emotion")
def websocket_emotion(websocket: WebSocket):
    websocket.accept()
    logger.info("WebSocket connection accepted")
    while True:
        try:
            # 接收base64编码的图片数据
            data = websocket.receive_text()
            
            # 解码base64数据
            image_data = base64.b64decode(data.split(',')[1])
            image = Image.open(io.BytesIO(image_data))
            
            # 进行情绪识别
            loop = asyncio.get_event_loop()
            result = loop.run_in_executor(executor, ImageController.get_emotion, image)
            
            # 发送识别结果
            websocket.send_text(result)
            logger.debug(f"识别结果: {result}")
        except Exception as e:
            logger.error(f"错误: {str(e)}")
            websocket.send_text(f"错误: {str(e)}")
            break
    
    websocket.close()
    logger.info("WebSocket connection closed")
