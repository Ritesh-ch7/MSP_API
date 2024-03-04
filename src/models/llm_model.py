from sqlalchemy import Column, Integer, Enum, String, DateTime, Text
from src.config.database import base
import enum
from datetime import datetime
 
 
class LLM(base):
    __tablename__ = "LLM_job_details"
 
    Id = Column(Integer,primary_key=True,autoincrement=True)
    TicketId = Column(Integer, unique=True)
    RequestorName = Column(String(50))
    Severity = Column(Integer)
    Priority = Column(Enum('Low','Medium','High'), default='Low')
    TicketType = Column(Enum('Incident','Service'))
    Service = Column(Enum('Phonecall', 'Email'))
    Description = Column(String(100))
 


 
