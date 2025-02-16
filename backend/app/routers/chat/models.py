from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.main import Base
import datetime


class Chat(Base):
    __tablename__ = "chat_data"
    chat_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    message = Column(String, default="")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
