import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.utils.snake_case_to_pascal import snake_to_pascal
from src.database import session_local, engine
from src import models
from sqlalchemy.orm import Session
from src.controllers.database_controllers.tasks_db.update_status import update_task_status
from src.constants import *
from sqlalchemy import func

async def update_task_response(task_id, generated_response, db,  trace_id):
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
       
       db.query(models.Task).filter(models.Task.Id == task_id).update({models.Task.Response : generated_response, models.Task.UpdatedAt : func.now()})
       db.commit()
       update_task_status(task_id, db, 'Completed', trace_id)
       logger.debug(f'{trace_id} response for task with task id {task_id} is updated')
        

    except Exception as e:
        logger.error(f'{trace_id} Could not add response to the task with id {task_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Cannot update the response of the task, {e}')