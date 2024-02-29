from fastapi import APIRouter,Depends, Request
from fastapi.responses import Response
import uuid
from src.controllers.email_controllers import generate_email
from src.services.validate_input import validate_input_data
from fastapi.responses import JSONResponse
from src.config.logger_config import new_logger as logger
from sqlalchemy.orm import Session
from src.config.database import session_local, engine
# from src import models
from src.controllers.database_controllers.llm_jobs_db.llmjob import add_to_llmjob_table
from src.controllers.database_controllers.tasks_db.tasks import add_task
from src.controllers.database_controllers.tasks_db.update_status import update_task_status
from src.services.regenerate_service import regenerate_mail_template
from src.controllers.database_controllers.tasks_db.update_response import update_task_response
from src.utils.constants import *
from src.models.llm_model import LLM
from src.models.task_model import Task
from src.config.database import base

models = [LLM,Task]

base.metadata.create_all(bind=engine, tables=[model.__table__ for model in models])
def get_db():  
    db = session_local()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/{user_id}/email")
async def user_data(user_id, request : Request, db :Session = Depends(get_db), trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    
    try:
        response = await validate_input_data(request, trace_id)

        llm_id = add_to_llmjob_table(response['validated_item'], db, trace_id)
        task_id = add_task(llm_id, response['reference_list'], user_id, db, trace_id)
        
    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = INTERNAL_SERVER_ERROR)
    
    try:
        update_task_status(task_id, db, 'Inprogress', trace_id)
        email_response = await generate_email(response,llm_id,trace_id)
        print(email_response)
        res = email_response.body.decode('utf-8')

        res_with_newline=res.replace("\\n","\n")

        await update_task_response(task_id, res_with_newline,db,trace_id)
        
        logger.info("Email generated successfully")
        email_with_newline=Response(content=res_with_newline, media_type="text/plain")
        return email_with_newline
    
    except Exception as e:
        logger.error(f"{trace_id} : Task has been terminated {e}")
        error_msg = f"Error in updating the task: {str(e)}"
        update_task_status(task_id, db, 'Failed', trace_id)
        return JSONResponse(content={"message": error_msg}, status_code = INTERNAL_SERVER_ERROR)


@router.post("/{user_id}/regenerate")
async def regenerate(request : Request, db :Session = Depends(get_db), trace_id:str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        request_data = await request.json()
        body = request_data.get('body',None)
        llm_id = request_data.get('llm_id',None)
        if body and llm_id:
            regenerated_mail = regenerate_mail_template(body)
            return JSONResponse(content={"message":regenerated_mail},status_code = OK)
        else:
            error_msg = f"body or llm_id is missing in request body"
            return JSONResponse(content={"message":error_msg},status_code = UNPROCESSABLE_ENTITY)
    except Exception as e:
        error_msg = f"Error in regenerate mail : {e}"
        return JSONResponse(content={"message":error_msg},status_code = INTERNAL_SERVER_ERROR)

    
