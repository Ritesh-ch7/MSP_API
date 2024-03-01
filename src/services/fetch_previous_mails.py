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

async def fetch_prev_mails(llm_id, db, trace_id):
    if(not trace_id):
        trace_id = str(uuid.uuid4())

    try:
       
        previous_mails = list(db.query(Task.Response['body']).filter(Task.LlmId == llm_id))
        logger.debug(f'{trace_id} all previous mails for the llm_id {llm_id} are fetched')
        return previous_mails
        

    except Exception as e:
        logger.error(f'{trace_id} Could not add fetch previous mails of llm_id {llm_id}')
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'Could not add fetch previous mails of llm_id {llm_id}')