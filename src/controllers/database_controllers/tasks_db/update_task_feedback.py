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

async def update_task_feedback(llm_id, db, task_feedback, user_id, trace_id):
    """
    Updates the feedback for a task with the specified LLM (Large Language Model) ID in the database.

    Args:
    - llm_id: The LLM ID associated with the task to be updated.
    - db: The database session to perform the database operations.
    - task_feedback: The feedback to be updated for the task.
    - user_id: The ID of the user updating the task feedback.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.

    Raises:
    HTTPException: If an error occurs during the database operation, 
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
       task = db.query(Task).filter(Task.LlmId == llm_id).order_by(Task.Id.desc()).first()
       task.Feedback = task_feedback 
       task.UpdatedAt = func.now()
       task.UpdatedBy = user_id
       db.commit()

       logger.debug(f'{trace_id} Feedback for the task with llm_id {llm_id} has been updated to {task_feedback}')


    except Exception as e:
        logger.error(f'{trace_id} Could not update the feedback of the task with id {llm_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Cannot update the feedback of the task, {e}')