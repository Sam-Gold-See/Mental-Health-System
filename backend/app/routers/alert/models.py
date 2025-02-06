from sqlmodel import SQLModel, Field
import datetime

class Alert(SQLModel, table=True):
    alert_id     : str               = Field(primary_key=True)
    user_id      : str               = Field(foreign_key="users.user_id")
    alert_type   : str               = Field(default="")
    alert_message: str               = Field(default="")
    created_at   : datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
