import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.utils.snake_case_to_pascal import snake_to_pascal
from src.config.database import session_local, engine
from src.models.llm_model import LLM
from sqlalchemy.orm import Session
from src.utils.constants import *


def add_to_llmjob_table(ticket : Ticket, db:Session, trace_id : str = None):
    if(trace_id == None):
        trace_id = str(uuid.uuid4())

    try: 
        llm_job = db.query(LLM).filter(LLM.TicketId == ticket.ticket_id).first()
        if llm_job:
            raise Exception
        
    except Exception as e:
        raise HTTPException(status_code = BAD_REQUEST, detail = f'ticket with id {ticket.ticket_id} is already present in the database')
    
    try:
        
        llm_job_record = {
            snake_to_pascal('ticket_type'): ticket.ticket_type.value,
            snake_to_pascal('service'): ticket.service.value,
            snake_to_pascal('priority'): ticket.priority.value,
            snake_to_pascal('severity'): ticket.severity,
            snake_to_pascal('requestor_name'): ticket.requestor_name,
            snake_to_pascal('description'): ticket.description,
            snake_to_pascal('ticket_id'): ticket.ticket_id
        }

        llm_job_record = LLM(**llm_job_record)
        db.add(llm_job_record)
        db.commit()
        db.refresh(llm_job_record)
        
        logger.debug(f'{trace_id} new llm job with id {llm_job_record.Id} is created')
        return llm_job_record.Id
    
    except Exception as e:
        logger.error(f'{trace_id} Could not add ticket deatils of ticket id {ticket.ticket_id} to the database')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Error in DB : Could not add ticket deatils of ticket id {ticket.ticket_id} to the database, {e}')