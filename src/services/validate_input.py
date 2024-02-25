from fastapi import Request,HTTPException
from fastapi.encoders import jsonable_encoder
from src.schemas.users import *
import uuid
from src.config.logger_config import new_logger as logger

async def validate_input_data(request: Request,trace_id:str = None):
    if trace_id == None:
        trace_id = str(uuid.uuid4())
    try:
        data = await request.json()
        item_dict = jsonable_encoder(data)
        reference_list = data.get("reference", [])
        required_keys = {"ticket_type", "service", "priority", "severity", "requestor_name", "message", "ticket_id","reference"}

        # ticket_data = {
        #     "ticket_type": data["ticket_type"],
        #     "service": data["service"],
        #     "priority": data["priority"],
        #     "severity": data["severity"],
        #     "requestor_name": data["requestor_name"],
        #     "message": data["message"],
        #     "ticket_id": data["ticket_id"],
        # }

        if not set(item_dict.keys()) == required_keys:
            raise HTTPException(status_code=400, detail="All required keys must be present in the request")

        if data["ticket_type"] not in [e.value for e in TicketType]:
            raise HTTPException(status_code=400, detail="Invalid entry value for ticket_type in the request: expected Incident or Service")

        if data["service"] not in [e.value for e in Service]:
            raise HTTPException(status_code=400, detail="Invalid entry value for service in the request: expected Phonecall or Email")

        if data["priority"] not in [e.value for e in Priority]:
            raise HTTPException(status_code=400, detail="Invalid entry value for priority in the request: expected Low, Medium, or High")

        if not isinstance(data["severity"], int) and not (data["severity"] > 4 and data["severity"]<=0) :
            raise HTTPException(status_code=400, detail="Invalid data type in the severity: int from 1 to 4")

        if not isinstance(data["requestor_name"], str):
            raise HTTPException(status_code=400, detail="Invalid data type in requester name: expected string")

        if not isinstance(data["message"], str):
            raise HTTPException(status_code=400, detail="Invalid data type in the message: expected string")

        if not isinstance(data["ticket_id"], int):
            raise HTTPException(status_code=400, detail="Invalid data type in the ticket_id: expected int")
        # print({Ticket(**ticket_data),reference_list})
        # return {Ticket(**ticket_data),reference_list}
        print("Here")
        validated_item = Ticket(**data)
        return {"validated_item": validated_item, "reference_list": reference_list}

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
