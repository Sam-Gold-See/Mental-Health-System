from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.main import Base
import datetime


class Alert(Base):
    __tablename__ = "alerts"
    alert_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    alert_type = Column(String, default="")
    alert_message = Column(String, default="")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
