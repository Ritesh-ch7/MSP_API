from fastapi import Request,HTTPException,Request
from fastapi.encoders import jsonable_encoder
from src.services.validate_reference import validate_reference_list
from src.schemas.users import *
import uuid
from src.utils.constants import *
from src.config.logger_config import new_logger as logger
from src.services.add_missing_fields import add_missing_fields


async def validate_input_data(request: Request,trace_id:str = None):
    if trace_id == None:
        trace_id = str(uuid.uuid4())
    try:
        data = await request.json()
        item_dict = jsonable_encoder(data)
        reference_list = data.get("reference", [])
        required_keys = {"ticket_type", "service", "priority", "severity", "requestor_name", "description", "ticket_id","reference"}

        if not set(item_dict.keys()) == required_keys:
            logger.error(f"{trace_id}: all keys required") 
            raise HTTPException(status_code=UNPROCESSABLE_ENTITY, message="All required keys must be present in the request")

        if data["ticket_type"] not in [e.value for e in TicketType]:
            logger.error(f"{trace_id}:Invalid entry value for ticket_type in the request: expected Incident or Service ") 
            raise HTTPException(status_code=UNPROCESSABLE_ENTITY, message="Invalid entry value for ticket_type in the request: expected Incident or Service")

        if data["service"] not in [e.value for e in Service]:
            logger.error(f"{trace_id}:Invalid entry value for service in the request: expected Phonecall or Email") 
            raise HTTPException(status_code=UNPROCESSABLE_ENTITY, message="Invalid entry value for service in the request: expected Phonecall or Email")

        if data["priority"] not in [e.value for e in Priority]:
            logger.error(f"{trace_id}:Invalid entry value for priority in the request: expected Low, Medium, or High")
            raise HTTPException(status_code=UNPROCESSABLE_ENTITY, message="Invalid entry value for priority in the request: expected Low, Medium, or High")

        if not isinstance(data["severity"], int) and not (data["severity"] > 4 and data["severity"]<=0) :
            logger.error(f"{trace_id}:Invalid data type in the severity: int from 1 to 4")
            raise HTTPException(status_code=UNPROCESSABLE_ENTITY, message="Invalid data type in the severity: int from 1 to 4")

        if not isinstance(data["requestor_name"], str):
            logger.error(f"{trace_id}:Invalid data type in requester name: expected string")
            raise HTTPException(status_code=UNPROCESSABLE_ENTITY, message="Invalid data type in requester name: expected string")

        if not isinstance(data["description"], str):
            logger.error(f"{trace_id}:Invalid data type in the description: expected string")
            raise HTTPException(status_code=UNPROCESSABLE_ENTITY, message="Invalid data type in the description: expected string")

        if not isinstance(data["ticket_id"], int):
            logger.error(f"{trace_id}:Invalid data type in the ticket_id: expected int")
            raise HTTPException(status_code=UNPROCESSABLE_ENTITY, message="Invalid data type in the ticket_id: expected int")
        
        validate_reference_list(reference_list)

        for i in range(0,len(reference_list)):
            reference_list[i] = add_missing_fields(reference_list[i])
        print(reference_list)
         
        validated_item = Ticket(**item_dict)
        logger.debug(f"{trace_id}: Input is validated")
        return {"validated_item": validated_item, "reference_list": reference_list}

    except HTTPException as http_exception:
        logger.error(f"{trace_id}:Error in data validation")
        raise http_exception

    except Exception as e:
        logger.error(f"{trace_id}:Fields in client side error")
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail=f"Error: {str(e)}")
