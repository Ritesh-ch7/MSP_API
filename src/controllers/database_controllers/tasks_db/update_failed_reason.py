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
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
       task = db.query(Task).filter(Task.Id == task_id)
       task.FailedReason = error_msg
       db.commit()


    except Exception as e:
        logger.error(f'{trace_id} Could not update the reason of failure for the task with id {task_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Could not update the reason of failure for the task with id {task_id}')