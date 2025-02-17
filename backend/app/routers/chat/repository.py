from typing import List, Tuple
from uuid import UUID, uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import ChatMessage, ChatMessageCreate


async def create_chat_messages(
    user_id: UUID,
    content: str,
    ai_response: str,
    session_id: UUID | None,
    sessionDB: AsyncSession,
) -> Tuple[ChatMessage, ChatMessage]:
    """创建用户消息和AI响应消息对"""
    final_session_id = session_id or uuid4()

    # 创建用户消息
    user_message = ChatMessage(
        message_id=str(uuid4()),
        user_id=str(user_id),
        role="user",
        content=content,
        session_id=str(final_session_id),
    )

    # 创建AI响应消息
    ai_message = ChatMessage(
        message_id=str(uuid4()),
        user_id=str(user_id),
        role="assistant",
        content=ai_response,
        session_id=str(final_session_id),
    )

    sessionDB.add(user_message)
    sessionDB.add(ai_message)

    return user_message, ai_message


async def get_chat_history(
    session_id: UUID, sessionDB: AsyncSession
) -> List[ChatMessage]:
    """获取聊天历史记录"""
    query = (
        select(ChatMessage)
        .where(ChatMessage.session_id == str(session_id))
        .order_by(ChatMessage.created_at.desc())
        .limit(10)  # 限制返回10条记录
    )
    result = await sessionDB.execute(query)
    return list(result.scalars().all())[::-1]
