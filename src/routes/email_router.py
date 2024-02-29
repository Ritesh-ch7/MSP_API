from fastapi import APIRouter,Depends, Request
from fastapi.responses import Response
import uuid
from src.controllers.email_controllers import generate_email
from src.services.validate_input import validate_input_data
from fastapi.responses import JSONResponse
from src.config.logger_config import new_logger as logger
from sqlalchemy.orm import Session
from src.controllers.database_controllers.llm_jobs_db.llmjob import add_to_llmjob_table
from src.controllers.database_controllers.tasks_db.tasks import add_task
from src.controllers.database_controllers.tasks_db.update_status import update_task_status
from src.controllers.database_controllers.tasks_db.update_response import update_task_response
from src.utils.constants import *
from src.config.get_db import get_db
from src.controllers.renegerate_controller import regenerate_mail

router = APIRouter()



@router.post("/{user_id}/email")
async def user_data(user_id, request : Request, db :Session = Depends(get_db), trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    
    try:
        response = await validate_input_data(request, trace_id)
        llm_id =  add_to_llmjob_table(response['validated_item'], db, trace_id)
        task_id =  add_task(llm_id, response['reference_list'], user_id, db, trace_id)
        
    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = INTERNAL_SERVER_ERROR)
    
    try:
        update_task_status(task_id, db, 'Inprogress', trace_id)
        print("herre")
        email_response = await generate_email(response,db,llm_id,task_id,trace_id)
        res = email_response.body.decode('utf-8')
        res_with_newline=res.replace("\\n","\n")

        
        logger.info("Email generated successfully")
        email_with_newline = Response(content=res_with_newline, media_type="text/plain")
        return email_with_newline
    
    except Exception as e:
        logger.error(f"{trace_id} : Task has been terminated {e}")
        error_msg = f"Error in updating the task: {str(e)}"
        update_task_status(task_id, db, 'Failed', trace_id)
        return JSONResponse(content={"message": error_msg}, status_code = INTERNAL_SERVER_ERROR)


@router.post("/{user_id}/regenerate")
async def regenerate(request : Request, user_id,  db :Session = Depends(get_db), trace_id:str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        regenerated_mail = await regenerate_mail(request,user_id, db, trace_id)

        res = regenerated_mail.body.decode('utf-8')
        res_with_newline=res.replace("\\n","\n")\
        
        email_with_newline = Response(content=res_with_newline, media_type="text/plain")

        return email_with_newline
    
    except Exception as e:
        error_msg = f"Error in regenerate : main : {e}"
        return JSONResponse(content={"message":error_msg},status_code = INTERNAL_SERVER_ERROR)

    
