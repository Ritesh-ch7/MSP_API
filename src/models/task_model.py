from sqlalchemy import Column, Integer, Enum, String, DateTime, Text
# from sqlalchemy.dialects.mysql import Text,LONGTEXT
from src.database import base
import enum
from datetime import datetime

class FeedbackEnum(enum.Enum):
    Positive = "Positive"
    Negative = "Negative"

class StatusEnum(enum.Enum):
    Pending = 'Pending'
    Inprogress = 'Inprogress'
    Completed = 'Completed'
    Failed = 'Failed'

class Task(base):
    __tablename__ = "tasks"

    Id = Column(Integer,primary_key=True,autoincrement=True)
    LlmId = Column(Integer)
    Feedback = Column(Enum(FeedbackEnum),default=FeedbackEnum.Positive, nullable = False)
    FailedReason = Column(String(100))
    Response = Column(Text)
    Reference = Column(Text)
    Status = Column(Enum(StatusEnum))
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime)
    CreatedBy = Column(String(50))
    UpdatedBy = Column(String(50))