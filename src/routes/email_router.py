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
from src.controllers.database_controllers.tasks_db.update_failed_reason import update_failed_reason
from src.utils.constants import *
from src.config.get_db import get_db
from src.controllers.renegerate_controller import regenerate_mail

router = APIRouter()



@router.post("/{user_id}/email")
async def user_data(user_id, request : Request, db :Session = Depends(get_db), trace_id : str = None):
    """
    Processes user data, validates input, generates email, and updates task status accordingly.

    Args:
    - user_id: The ID of the user submitting the data.
    - request: The FastAPI Request object containing user data.
    - db: The database session to perform the database operations.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.

    Returns:
    A Response containing the generated email body.

    Raises:
    HTTPException: If an error occurs during the data processing, validation, or email generation, 
                   an HTTPException with the appropriate status code is raised.
    """
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    
    try:
        response = await validate_input_data(request, trace_id)
        llm_id =  add_to_llmjob_table(response['validated_item'], db, trace_id)
        task_id =  add_task(llm_id, response['reference_list'], user_id, db, trace_id)
        
    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = UNPROCESSABLE_ENTITY)
    
    try:
        update_task_status(task_id, db, 'Inprogress',user_id, trace_id)
        email_response = await generate_email(response,db,llm_id,task_id,user_id,trace_id)
        update_task_status(task_id, db, 'Completed', user_id, trace_id)
        res = email_response.body.decode('utf-8')
        res_with_newline=res.replace("\\n","\n")

        
        logger.info("Email generated successfully")
        email_with_newline = Response(content=res_with_newline, media_type="text/plain")
        return email_with_newline
    
    except Exception as e:
        logger.error(f"{trace_id} : Task has been terminated {e}")
        error_msg = f"Error in updating the task: {str(e)}"
        update_task_status(task_id, db, 'Failed', user_id, trace_id)
        update_failed_reason(task_id,db,error_msg,trace_id)
        return JSONResponse(content={"message": error_msg}, status_code = INTERNAL_SERVER_ERROR)


@router.post("/{user_id}/regenerate")
async def regenerate(request : Request, user_id,  db :Session = Depends(get_db), trace_id:str = None):
    """
    Regenerates an email based on the provided email body, subject, and language model ID.

    Args:
    - request: The FastAPI Request object containing the JSON body with 'body', 'subject', and 'llm_id'.
    - user_id: The ID of the user regenerating the email.
    - db: The database session to perform the database operations.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.

    Returns:
    A Response containing the regenerated email body.

    Raises:
    HTTPException: If an error occurs during the email regeneration or database operation, 
                   an HTTPException with the appropriate status code is raised.
    """
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        regenerated_mail = await regenerate_mail(request,user_id, db, trace_id)
        

        res = regenerated_mail.body.decode('utf-8')
        res_with_newline=res.replace("\\n","\n")\
        
        email_with_newline = Response(content=res_with_newline, media_type="text/plain")

        logger.info(f'{trace_id} regenerated email has been sent successfully !!')

        return email_with_newline
    
    except Exception as e:
        error_msg = f"Error in regenerate : main : {e}"
        
        return JSONResponse(content={"message":error_msg},status_code = INTERNAL_SERVER_ERROR)

    
