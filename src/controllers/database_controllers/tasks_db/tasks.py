import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.utils.snake_case_to_pascal import snake_to_pascal
from src.config.database import session_local, engine
# from src import models
from src.models.task_model import Task
import json
from sqlalchemy.orm import Session
from src.utils.constants import *

def add_task(llm_id, reference_list, user_id, db, trace_id : str = None):
    """
    Adds a new task to the database with the provided parameters.

    Args:
    - llm_id: The ID associated with the Large Language Model (LLM) for the task.
    - reference_list: A list of reference items associated with the task.
    - user_id: The ID of the user creating the task.
    - db: The database session to perform the database operations.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.

    Returns:
    The ID of the newly created task.

    Raises:
    HTTPException: If an error occurs during the task creation, 
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    if(not trace_id):
        trace_id = str(uuid.uudi4())
    
    try:
        task_record = {
            snake_to_pascal('llm_id'): llm_id,
            snake_to_pascal('reference'): json.dumps(reference_list),
            snake_to_pascal('status'): 'Pending',
            snake_to_pascal('created_by'): user_id
        }

        task_record = Task(**task_record)
        db.add(task_record)
        db.commit()
        db.refresh(task_record)
        logger.debug(f'{trace_id} new task with id {task_record.Id} is created')
        return task_record.Id

    except Exception as e:
        logger.error(f'{trace_id} Could not create task for given llm_id {llm_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Could not create task for given llm_id {llm_id}, {e}')