from sqlalchemy import Column, Integer, Enum, String, DateTime, Text
from src.config.database import base
import enum
from datetime import datetime
 
 
class LLM(base):
    __tablename__ = "LLM_job_details"
 
    Id = Column(Integer,primary_key=True,autoincrement=True)
    TicketId = Column(String(20), unique=True)
    RequestorName = Column(String(50),nullable = True)
    Severity = Column(Enum('Critical','High','Medium','Low'),nullable = True)
    Priority = Column(Enum('Low','Medium','High'), default='Low')
    TicketType = Column(Enum('Incident','Service Request'),nullable = True)
    Source = Column(Enum('Phonecall', 'Email'),nullable = True)
    Title = Column(Text)
    Description = Column(Text)
    Status = Column(Enum('Assigned','Closed','Inprogress'))
    CompanyName= Column(Text,nullable = True)