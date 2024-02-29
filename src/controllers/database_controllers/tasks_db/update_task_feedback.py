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

async def update_task_feedback(llm_id, db, trace_id):
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
        task = db.query(Task).filter(Task.LlmId == llm_id).order_by(Task.Id.desc()).first()
        if task:
            task.Feedback = 'Negative'
            task.UpdatedAt = func.now()
            db.commit()

    except Exception as e:
        logger.error(f'{trace_id} Could not update the feedback of the task with id {llm_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Cannot update the feedback of the task, {e}')