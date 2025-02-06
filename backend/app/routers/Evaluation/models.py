from sqlmodel import SQLModel, Field
import datetime

class Evaluation(SQLModel, table=True):
    evaluation_id      : str               = Field(primary_key=True)
    user_id            : str               = Field(foreign_key="users.user_id")
    mental_health_score: int               = Field(default=0)
    evaluation_result  : str               = Field(default="")
    created_at         : datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
