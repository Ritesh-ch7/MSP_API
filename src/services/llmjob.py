import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.services.utils.snake_case_to_pascal import snake_to_pascal
from src.database import session_local, engine
from src import models
from sqlalchemy.orm import Session


def add_to_llmjob_table(ticket : Ticket, db:Session, trace_id : int = None):
    if(trace_id == None):
        trace_id = str(uuid.uuid4())

    try: 
        ticket = ticket['validated_item']
        llm_job_record = {
            snake_to_pascal('ticket_type'): ticket.ticket_type.value,
            snake_to_pascal('service'): ticket.service.value,
            snake_to_pascal('priority'): ticket.priority.value,
            snake_to_pascal('severity'): ticket.severity,
            snake_to_pascal('requestor_name'): ticket.requestor_name,
            snake_to_pascal('message'): ticket.message,
            snake_to_pascal('ticket_id'): ticket.ticket_id
        }

        llm_job_record = models.LLM(**llm_job_record)
        db.add(llm_job_record)
        db.commit()
        db.refresh(llm_job_record)
        return True
    
    except Exception as e:
        logger.error(f'{trace_id} Could not add ticket deatils of ticket id {ticket.ticket_id} to the database')
        raise HTTPException(status_code = 500, detail = f'Cannot add the record to the database, {e}')