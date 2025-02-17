from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, UUID4
from typing import Optional

from app.db.main import get_session
from app.dependencies import get_current_user
from .controller import ChatController
from app.routers.chat.models import ChatMessageCreate
from app.routers.chat.repository import get_chat_history

router = APIRouter(
    prefix="/chat", tags=["chat"], responses={404: {"description": "Not found"}}
)

chat_controller = ChatController()


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    system_prompt: Optional[str] = None
    content: str
    session_id: Optional[UUID4] = None


class ChatResponse(BaseModel):
    response: str
    session_id: UUID4


@router.post("/send")
async def 发送消息(
    chat_request: ChatRequest,
    user_id: UUID4 = Depends(get_current_user),
    sessionDB: AsyncSession = Depends(get_session),
) -> ChatResponse:
    try:
        message = ChatMessageCreate(
            content=chat_request.content, session_id=chat_request.session_id
        )
        response, session_id = await chat_controller.send_message(
            user_id=user_id,
            message=message,
            sessionDB=sessionDB,
            system_prompt=chat_request.system_prompt,
        )
        return ChatResponse(response=response, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天请求失败: {str(e)}")


@router.get("/history/{session_id}")
async def 获取聊天历史(
    session_id: UUID4,
    user_id: UUID4 = Depends(get_current_user),
    sessionDB: AsyncSession = Depends(get_session),
):
    history = await get_chat_history(session_id, sessionDB)
    return history
