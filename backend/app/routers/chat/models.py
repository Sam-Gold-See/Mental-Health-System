from sqlmodel import SQLModel, Field
import datetime

class Chat(SQLModel, table=True):
    __tablename__ = "chat_data"
    chat_id   : str               = Field(primary_key=True)
    user_id   : str               = Field(foreign_key="users.user_id")
    message   : str               = Field(default="")
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

