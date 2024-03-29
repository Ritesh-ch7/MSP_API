from sqlalchemy import Column, Integer, Enum, String, DateTime, Text, JSON, func
from src.config.database import base
import enum
from datetime import datetime

class Task(base):
    __tablename__ = "tasks"
 
    Id = Column(Integer,primary_key=True,autoincrement=True)
    LlmId = Column(Integer)
    Feedback = Column(Enum('Positive','Negative'),default='Positive')
    FailedReason = Column(String(100))
    Response = Column(JSON)
    Reference = Column(Text)
    Status = Column(Enum('Pending', 'Inprogress', 'Completed', 'Failed'))
    CreatedAt = Column(DateTime, default=func.now())
    UpdatedAt = Column(DateTime)
    CreatedBy = Column(String(50))
    UpdatedBy = Column(String(50))