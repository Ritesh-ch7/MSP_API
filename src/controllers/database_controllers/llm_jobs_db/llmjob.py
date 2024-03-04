import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.utils.snake_case_to_pascal import snake_to_pascal
from src.config.database import session_local, engine
from src.models import llm_model
from sqlalchemy.orm import Session
from src.utils.constants import *


def create_llmjob(ticket : Ticket, db:Session, trace_id : str = None):
    """
    Creates a new LLM job record based on the provided ticket details and adds it to the database.

    Parameters:
    - ticket (Ticket): The Ticket object containing details for the new LLM job.
    - db (Session): The database session object to interact with the database.
    - trace_id (str, optional): Unique identifier for tracking the operation. If not provided, a new UUID is generated.

    Returns:
    int: The ID of the newly created LLM job.

    Raises:
    HTTPException: If there is an error adding the ticket details to the database.
    """
    if(trace_id == None):
        trace_id = str(uuid.uuid4())

    try: 
        # ticket = ticket['validated_item']
        llm_job_record = {
            snake_to_pascal('ticket_type'): ticket.ticket_type.value,
            snake_to_pascal('service'): ticket.service.value,
            snake_to_pascal('priority'): ticket.priority.value,
            snake_to_pascal('severity'): ticket.severity,
            snake_to_pascal('requestor_name'): ticket.requestor_name,
            snake_to_pascal('description'): ticket.description,
            snake_to_pascal('ticket_id'): ticket.ticket_id
        }

        llm_job_record = llm_model.LLM(**llm_job_record)
        db.add(llm_job_record)
        db.commit()
        db.refresh(llm_job_record)
        
        logger.debug(f'{trace_id} new llm job with id {llm_job_record.Id} is created')
        return llm_job_record.Id
    
    except Exception as e:
        logger.error(f'{trace_id} Could not add ticket deatils of ticket id {ticket.ticket_id} to the database')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Cannot add the record to the database, {e}')