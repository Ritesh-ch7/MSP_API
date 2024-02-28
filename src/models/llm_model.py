from sqlalchemy import Column, Integer, Enum, String, DateTime, Text
# from sqlalchemy.dialects.mysql import Text,LONGTEXT
from src.database import base
import enum
from datetime import datetime

class PriorityEnum(enum.Enum):
    High = 'High'
    Medium = 'Medium'
    Low = 'Low'
    
class TickettypeEnum(enum.Enum):
    Incident = "Incident"
    Service = "Service"

class ServiceEnum(enum.Enum):
    Phonecall = "Phonecall"
    Email = "Email"

class LLM(base):
    __tablename__ = "LLM_job_details"

    Id = Column(Integer,primary_key=True,autoincrement=True)
    TicketId = Column(Integer, unique=True)
    RequestorName = Column(String(50))
    Severity = Column(Integer)
    Priority = Column(Enum(PriorityEnum), default='Low')
    TicketType = Column(Enum(TickettypeEnum))
    Service = Column(Enum(ServiceEnum))
    Description = Column(String(100))