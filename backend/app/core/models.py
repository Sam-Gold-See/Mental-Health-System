from sqlalchemy import Column, String, DateTime, ForeignKey
from app.db.main import Base
import datetime


class Emotion_Model(Base):
    __tablename__ = "emotion_analysis"
    analysis_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    text_emotion = Column(String, default="")
    image_emotion = Column(String, nullable=True)
    eeg_emotion = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )

