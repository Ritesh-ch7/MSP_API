from enum import Enum
from pydantic import BaseModel
from typing import Optional
class TicketType(str, Enum):
    Incident = "Incident"
    Service = "Service Request"


class Priority(str, Enum):
    High = "High"
    Medium = "Medium"
    Low = "Low"

class Source(str, Enum):
    Phonecall = "Phonecall"
    Email = "Email"

class Status(str, Enum):
    Assigned = "Assigned"
    Closed = "Closed"
    Inprogress = "Inprogress"

class Severity(str, Enum):
    Critical = "Critical"
    High = "High"
    Medium = "Medium"
    Low = "Low"

class Ticket(BaseModel):
    ticket_id: str
    ticket_type: TicketType
    priority: Priority
    severity: Severity
    requestor_name: Optional[str] = None
    description: Optional[str] = None
    source: Optional[Source] = None
    title: str
    status: Status
    company_name: Optional[str] = None
    sla: str