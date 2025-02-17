from typing import List, Tuple
from uuid import UUID
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.chat.models import ChatMessageCreate, ChatMessage
from app.routers.chat.repository import get_chat_history, create_chat_messages
from app.config import config


class ChatController:
    def __init__(self):
        self._init_chat_model()

    def _init_chat_model(self) -> None:
        """初始化聊天模型"""
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.chat_model: ChatOpenAI = ChatOpenAI(
            temperature=0.7,
            streaming=True,
            callback_manager=callback_manager,
            verbose=True,
            model=config.OPENAI_MODEL,
            base_url=config.OPENAI_BASE_URL,
            api_key=config.OPENAI_API_KEY,
        )

    def _prepare_langchain_messages(
        self, system_prompt: str | None, history_messages: List[ChatMessage]
    ) -> List[BaseMessage]:
        """准备 LangChain 消息格式"""
        langchain_messages = []
        if system_prompt:
            langchain_messages.append(SystemMessage(content=system_prompt))

        for msg in history_messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))
        return langchain_messages

    async def _generate_ai_response(
        self, messages: List[BaseMessage], temperature: float
    ) -> str:
        """生成 AI 响应"""
        self.chat_model.temperature = temperature
        response = await self.chat_model.agenerate([messages])
        return response.generations[0][0].text

    async def send_message(
        self,
        user_id: UUID,
        message: ChatMessageCreate,
        sessionDB: AsyncSession,
        system_prompt: str | None = None,
        temperature: float = 0.7,
    ) -> Tuple[str, UUID]:
        """处理发送消息的主流程"""
        async with sessionDB.begin():
            # 获取历史消息
            history_messages = []
            if message.session_id:
                history_messages = await get_chat_history(message.session_id, sessionDB)

            # 准备 LangChain 消息并添加当前消息
            langchain_messages = self._prepare_langchain_messages(
                system_prompt, history_messages
            )
            langchain_messages.append(HumanMessage(content=message.content))

            # 生成 AI 响应
            ai_response = await self._generate_ai_response(
                langchain_messages, temperature
            )

            # 保存消息对
            user_message, _ = await create_chat_messages(
                user_id=user_id,
                content=message.content,
                ai_response=ai_response,
                session_id=message.session_id,
                sessionDB=sessionDB,
            )

            return ai_response, UUID(user_message.session_id)
