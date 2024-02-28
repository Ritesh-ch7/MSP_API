from fastapi import APIRouter,Depends, Request
import uuid
from src.controllers.email_controllers import generate_email
from src.services.validate_input import validate_input_data
from fastapi.responses import JSONResponse
from src.config.logger_config import new_logger as logger
from sqlalchemy.orm import Session
from src.database import session_local, engine
from src import models
from src.controllers.database_controllers.llm_jobs_db.llmjob import add_to_llmjob_table
from src.controllers.database_controllers.tasks_db.tasks import add_task
from src.controllers.database_controllers.tasks_db.update_status import update_task_status
from src.controllers.database_controllers.tasks_db.update_response import update_task_response
from src.constants import *

models.base.metadata.create_all(bind = engine)
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
        await update_task_response(task_id, res,db,trace_id)
        
        logger.info("Email generated successfully")
        return email_response
    
    except Exception as e:
        logger.error(f"{trace_id} : Task has been terminated {e}")
        error_msg = f"Error in updating the task: {str(e)}"
        update_task_status(task_id, db, 'Failed', trace_id)
        return JSONResponse(content={"message": error_msg}, status_code = INTERNAL_SERVER_ERROR)


    
