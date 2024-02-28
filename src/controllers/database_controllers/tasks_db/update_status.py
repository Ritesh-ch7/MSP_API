import os, uuid
from src.config.logger_config import new_logger as logger
from src.schemas.users import *
from fastapi import HTTPException, Depends
from src.utils.snake_case_to_pascal import snake_to_pascal
from src.database import session_local, engine
# from src import models
from src.models.task_model import Task
from sqlalchemy.orm import Session
from datetime import datetime
from src.utils.constants import *
from sqlalchemy import func

def update_task_status(task_id, db, task_status, trace_id):
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
       db.query(Task).filter(Task.Id == task_id).update({Task.Status : task_status, Task.UpdatedAt : func.now()})
       db.commit()

    except Exception as e:
        logger.error(f'{trace_id} Could not update the status of the task with id {task_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Cannot update the status of the task, {e}')