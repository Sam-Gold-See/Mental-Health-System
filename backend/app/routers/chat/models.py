import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel

from app.db.main import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id: Mapped[UUID] = mapped_column(String, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(String, ForeignKey("users.user_id"))
    role: Mapped[str] = mapped_column(String(20))  # user 或 assistant
    content: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
    session_id: Mapped[UUID] = mapped_column(String)


class ChatMessageCreate(BaseModel):
    content: str
    session_id: Optional[UUID] = None
