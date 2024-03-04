import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.utils.snake_case_to_pascal import snake_to_pascal
from src.config.database import session_local, engine
from src.models import llm_model,tasks_model
from sqlalchemy.orm import Session
from datetime import datetime
from src.utils.constants import *
from sqlalchemy import func

def update_task_status(task_id, db, task_status, trace_id):
    """
    Updates the status of a task with the specified task ID in the database.

    Args:
    - task_id: The ID of the task to be updated.
    - db: The database session to perform the database operations.
    - task_status: The new status to be set for the task.
    - trace_id: A unique identifier for tracing purposes.

    Raises:
    HTTPException: If an error occurs during the database operation, 
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
       db.query(tasks_model.Task).filter(tasks_model.Task.Id == task_id).update({tasks_model.Task.Status : task_status, tasks_model.Task.UpdatedAt : func.now()})
       db.commit()

    except Exception as e:
        logger.error(f'{trace_id} Could not update the status of the task with id {task_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Cannot update the status of the task, {e}')