from fastapi import HTTPException
from typing import List
from src.schemas.users import *
import uuid
from src.config.logger_config import new_logger as logger

def validate_reference_item(item):
    if "ref" not in item:
        raise HTTPException(status_code=422, detail="Missing 'ref' attribute in the reference item")

    if 'ticket_type' in item and item['ticket_type'] not in [e.value for e in TicketType]:
        raise HTTPException(status_code=422, detail="Invalid entry value for ticket_type in the reference item: expected Incident or Service")

    if 'service' in item and item['service'] not in [e.value for e in Service]:
        raise HTTPException(status_code=422, detail="Invalid entry value for service in the reference item: expected Phonecall or Email")

    if 'priority' in item and item["priority"] not in [e.value for e in Priority]:
        raise HTTPException(status_code=422, detail="Invalid entry value for priority in the reference item: expected Low, Medium, or High")
    item["severity"]=int(item["severity"])
    if 'severity' in item and (not isinstance(item["severity"], int) or not (1 <= item["severity"] <= 4)):
        raise HTTPException(status_code=422, detail="Invalid data type or value in severity in the reference item: expected int from 1 to 4")

    if 'requestor_name' in item and not isinstance(item["requestor_name"], str):
        raise HTTPException(status_code=422, detail="Invalid data type in requester name in the reference item: expected string")

    if 'text' in item and not isinstance(item.get('text'), str):
        raise HTTPException(status_code=422, detail="Invalid data type in text in the reference item: expected string")
    item["ticket_id"]=int(item["ticket_id"])
    if 'ticket_id' in item and not isinstance(item["ticket_id"], int):
        raise HTTPException(status_code=422, detail="Invalid data type in ticket_id in the reference item: expected int")

def validate_reference_list(reference_list: List[dict]):
    for item in reference_list:
        validate_reference_item(item)
