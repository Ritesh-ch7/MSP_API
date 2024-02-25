from fastapi import APIRouter,Depends
import uuid
from src.controllers.email_controllers import generate_email
from src.services.validate_input import validate_input_data
from fastapi.responses import JSONResponse
from src.config.logger_config import new_logger as logger
from sqlalchemy.orm import Session
from src.database import session_local, engine
from src import models
from src.services.llmjob import add_to_llmjob_table
from src.services.tasks import add_task
from src.services.update_task import update_task_status
from src.services.update_response import update_response

models.base.metadata.create_all(bind = engine)
def get_db():  
    db = session_local()
    try:
        yield db
    finally:
        db.close()
router = APIRouter()



@router.post("/{user_id}/email")
async def user_data(user_id, response: any = Depends(validate_input_data), db :Session = Depends(get_db), trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    # print("abc")
    try:
        llm_id = add_to_llmjob_table(response, db, trace_id)
        task_id = add_task(llm_id, response, user_id, db, trace_id)
        
    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = 500)
    
    try:
        update_task_status(task_id, db, 'Inprogress', trace_id)
        email_response = await generate_email(response,trace_id)
        update_response(task_id, email_response,db,trace_id)
        

        return email_response
    
    except Exception as e:
        logger.error(f"{trace_id} : Task has been terminated {e}")
        error_msg = f"Error in updating the task: {str(e)}"
        update_task_status(task_id, db, 'Failed', trace_id)
        return JSONResponse(content={"message": error_msg}, status_code = 500)


    
