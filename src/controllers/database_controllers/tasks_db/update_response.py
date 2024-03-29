import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.utils.snake_case_to_pascal import snake_to_pascal
from src.config.database import session_local, engine
# from src import models
from src.models.task_model import Task
from sqlalchemy.orm import Session
from src.controllers.database_controllers.tasks_db.update_status import update_task_status
from src.utils.constants import *
from sqlalchemy import func

async def update_task_response(task_id, generated_response, db, user_id, trace_id):

    """
    Updates the response for a task with the specified task ID in the database.
 
    Args:
    - task_id: The ID of the task to be updated.
    - generated_response: The response to be updated for the task.
    - db: The database session to perform the database operations.
    - user_id: The ID of the user updating the task response.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.
 
    Raises:
    HTTPException: If an error occurs during the database operation,
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
       
        task = db.query(Task).filter(Task.Id == task_id).update({Task.Response : generated_response, Task.UpdatedAt : func.now(), Task.UpdatedBy : user_id})
        db.commit()
        logger.debug(f'{trace_id} response for task with task id {task_id} is added to database')
        await update_task_status(task_id, db, 'Completed', user_id, trace_id)
        

    except Exception as e:
        logger.error(f'{trace_id} Could not add response to the task with id {task_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Cannot update the response of the task, {e}')