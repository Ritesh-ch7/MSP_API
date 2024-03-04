from fastapi import APIRouter,Depends, Request
import uuid
from src.controllers.email_controllers import generate_email
from src.services.validate_input import validate_input_data
from fastapi.responses import JSONResponse
from src.config.logger_config import new_logger as logger
from sqlalchemy.orm import Session
from src.config.database import session_local, engine
from src.models import llm_model, tasks_model
from src.controllers.database_controllers.llm_jobs_db.llmjob import create_llmjob
from src.controllers.database_controllers.tasks_db.tasks import create_task
from src.controllers.database_controllers.tasks_db.update_status import update_task_status
from src.controllers.database_controllers.tasks_db.update_response import update_task_response
from src.utils.constants import *

llm_model.base.metadata.create_all(bind = engine)
def get_db():  
    db = session_local()
    try:
        yield db
    finally:
        db.close()
router = APIRouter()



@router.post("/{user_id}/email")
async def user_data(user_id, request : Request, db :Session = Depends(get_db), trace_id : str = None):
    """
    Processes user data, validates input, adds to LLM job table, adds a task, updates task status, generates an email, and updates task response.

    Args:
    - user_id: The ID of the user submitting the data.
    - request (Request): The incoming HTTP request containing user data.
    - db (Session, optional): The database session to perform database operations. 
      Defaults to the dependency `get_db`.
    - trace_id (str, optional): A unique identifier for tracing purposes. 
      If not provided, a new UUID will be generated.

    Returns:
    JSONResponse: A JSON response containing the generated email body and associated LLM ID.
                  If successful, returns a status code of 200 (OK); otherwise, returns 500 (Internal Server Error).

    Raises:
    Exception: If an error occurs during the processing of user data, it is logged, and a 500 (Internal Server Error) response is returned.
    """
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    
    try:
        response = await validate_input_data(request, trace_id)

        llm_id = create_llmjob(response['validated_item'], db, trace_id)
        task_id = create_task(llm_id, response['reference_list'], user_id, db, trace_id)
        
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


    
