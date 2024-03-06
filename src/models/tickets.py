from src.config.database import base
from sqlalchemy import Column, Integer, Enum, String, DateTime, Text
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
 
 
 
class TicketBase(base):
    __tablename__="ticket_base"
 
    ticket_id=Column(Integer, primary_key=True)
    requestor_name=Column(String(50))
    severity = Column(Integer)
    priority = Column(Enum(PriorityEnum), default='Low')
    ticket_type = Column(Enum(TickettypeEnum))
    service = Column(Enum(ServiceEnum))
    description = Column(String(100))