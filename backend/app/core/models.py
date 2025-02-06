from sqlmodel import SQLModel, Field
import datetime


class Emotion_Model(SQLModel, table=True, alias="emotion"):
    __tablename__ = "emotion_analysis"
    analysis_id  : str               = Field(primary_key=True)
    user_id      : str               = Field(foreign_key="users.user_id")
    text_emotion : str               = Field(default="")
    image_emotion: str | None        = Field(default=None)
    eeg_emotion  : str | None        = Field(default=None)
    created_at   : datetime.datetime = Field(
        default_factory = lambda: datetime.datetime.now(datetime.timezone.utc)
    )

