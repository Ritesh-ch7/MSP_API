import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.services.utils.snake_case_to_pascal import snake_to_pascal
from src.database import session_local, engine
from src import models
import json
from sqlalchemy.orm import Session

def add_task(llm_id, ticket, user_id, db, trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uudi4())
    
    try:
        task_record = {
            snake_to_pascal('llm_id'): llm_id,
            snake_to_pascal('reference'): json.dumps(ticket['reference_list']),
            snake_to_pascal('status'): 'Pending',
            snake_to_pascal('created_by'): user_id
        }
        # ticket = ticket['validated_item']
        task_record = models.Task(**task_record)
        db.add(task_record)
        db.commit()
        db.refresh(task_record)
        return task_record.Id

    except Exception as e:
        logger.error(f'{trace_id} Could not create task for {ticket.ticket_id}')
        raise HTTPException(status_code = 500, detail = f'Cannot add the record to the database, {e}')