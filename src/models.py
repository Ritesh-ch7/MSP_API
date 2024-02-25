from sqlalchemy import Column, Integer, Enum, String, DateTime, Text
from src.database import base
import enum
from datetime import datetime

class PriorityEnum(enum.Enum):
    High = 'High'
    Medium = 'Medium'
    Low = 'Low'
    
class TickettypeEnum(enum.Enum):
    Incident = "Incident"
    ServiceRequest = "Service Request"

class ServiceEnum(enum.Enum):
    Phonecall = "Phonecall"
    Email = "Email"

class LLM(base):
    __tablename__ = "LLM_job_details"

    Id = Column(Integer,primary_key=True,autoincrement=True)
    TicketId = Column(Integer, unique=True)
    RequestorName = Column(String(50))
    Severity = Column(Integer)
    Priority = Column(Enum(PriorityEnum))
    TicketType = Column(Enum(TickettypeEnum))
    Service = Column(Enum(ServiceEnum))
    Message = Column(String(100))


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
    Feedback = Column(Enum(FeedbackEnum))
    FailedReason = Column(String(100))
    Response = Column(String(100))
    Reference = Column(Text)
    Status = Column(Enum(StatusEnum))
    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow)
    CreatedBy = Column(String(50))
    UpdatedBy = Column(String(50))