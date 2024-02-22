from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.schemas.users import *
import uuid
from src.config.logger_config import new_logger as logger

async def validate_input_data(request: Request,trace_id : str = None):
    if(trace_id == None):
        trace_id = str(uuid.uuid4())
    try:
        data = await request.json()
        item_dict = jsonable_encoder(data)
        required_keys = {"ticket_type", "service", "priority", "severity", "requestor_name", "message","ticket_id"}

        if not set(item_dict.keys()) == required_keys:
            error_msg = "All required keys must be present in the request"
            return JSONResponse(content={"message": error_msg}, status_code=500)

        if data["ticket_type"] not in [e.value for e in TicketType]:
            error_msg = "Invalid entry value for ticket_type in the request: expected Incident or Service"
            return JSONResponse(content={"message": error_msg}, status_code=500)

        if data["service"] not in [e.value for e in Service]:
            error_msg = "Invalid entry value for service in the request : expected Phonecall or Email"
            return JSONResponse(content={"message": error_msg}, status_code=500)

        if data["priority"] not in [e.value for e in Priority]:
            error_msg = "Invalid entry value for priority in the request: expected Low,Medium, or High"
            return JSONResponse(content={"message": error_msg}, status_code=500)

        if not isinstance(data["severity"], int) :
            error_msg = "Invalid data type in the severity: int from 1 to 4"
            return JSONResponse(content={"message": error_msg}, status_code=500)

        if not isinstance(data["requestor_name"],str):
            error_msg = "Invalid data type in requester name : expected string"
            return JSONResponse(content={"message": error_msg}, status_code=500)

        if not isinstance(data["message"], str) :
            error_msg = "Invalid data type in the message: expected string"
            return JSONResponse(content={"message": error_msg}, status_code=500)

        if not isinstance(data["ticket_id"],int):
            error_msg = "Invalid data type in the ticket_id: expected int"
            return JSONResponse(content={"message": error_msg}, status_code=500)


        ticket = Ticket(**data)
        return ticket

    except Exception as e:

        error_msg = f"Internal Server Error: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code=500)
