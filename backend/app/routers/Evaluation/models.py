from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.db.main import Base
import datetime


class Evaluation(Base):
    __tablename__ = "mental_health_evaluation"
    evaluation_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    mental_health_score = Column(Integer, default=0)
    evaluation_result = Column(String, default="")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
