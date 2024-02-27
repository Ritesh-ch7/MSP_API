from enum import Enum
from pydantic import BaseModel

class TicketType(str, Enum):
    Incident = "Incident"
    Service = "Service"

class Service(str, Enum):
    Phonecall = "Phonecall"
    Email = "Email"

class Priority(str, Enum):
    High = "High"
    Medium = "Medium"
    Low = "Low"

class Ticket(BaseModel):
    ticket_type: TicketType
    service: Service
    priority: Priority
    severity: int
    requestor_name: str
    message: str
    ticket_id: int