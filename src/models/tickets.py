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
    Service = "Service Request"
 
class SourceEnum(enum.Enum):
    Phonecall = "Phonecall"
    Email = "Email"
 
class StatusEnum(enum.Enum):
    Assigned ='Assigned'
    Closed = 'Closed'
    AutoResolved ='AutoResolved'
    Inprogress = 'Inprogress'
 
class SeverityEnum(enum.Enum):
    Severity1 = "Severity1"
    Severity2 = "Severity1"
    Severity3 = "Severity3"
    Severity4 = "Severity4"
 
class TicketBase(base):
    __tablename__="ticket_base"
 
    id=Column(Integer, primary_key=True)
    ticket_id = Column(String(30))
    requestor_name=Column(String(100),nullable = True)
    title = Column(String(2000))
    description = Column(Text)
    status = Column(Enum('Assigned', 'Inprogress', 'Closed', 'AutoResolved'))
    severity = Column(Enum('Critical', 'High', 'Medium', 'Low'))
    priority = Column(Enum('Low', 'Medium', 'High'), default='Low')
    ticket_type = Column(Enum('Service Request', 'Incident'), nullable = True)
    source = Column(Enum('Email', 'Phonecall'), nullable = True)
    company_name = Column(Text,nullable = True)
    sla = Column(Text, nullable = True)