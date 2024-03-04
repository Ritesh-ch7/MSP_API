import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.utils.snake_case_to_pascal import snake_to_pascal
from src.config.database import session_local, engine
# from src import models
from src.models.task_model import Task
from sqlalchemy.orm import Session
from datetime import datetime
from src.utils.constants import *
from sqlalchemy import func

async def update_failed_reason(task_id, db, error_msg, trace_id):
    """
    Updates the failure reason for a task with the specified task ID in the database.

    Args:
    - task_id: The ID of the task to be updated.
    - db: The database session to perform the database operations.
    - error_msg: The error message to be set as the failure reason.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.

    Raises:
    HTTPException: If an error occurs during the database operation, 
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
       db.query(Task).filter(Task.Id == task_id).update({Task.FailedReason : error_msg})
       db.commit()


    except Exception as e:
        logger.error(f'{trace_id} Could not update the reason of failure for the task with id {task_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Could not update the reason of failure for the task with id {task_id}')