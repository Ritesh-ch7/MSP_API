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

models.base.metadata.create_all(bind = engine)
def get_db():  
    db = session_local()
    try:
        yield db
    finally:
        db.close()
router = APIRouter()



@router.post("/email")
async def user_data(response: any = Depends(validate_input_data), db :Session = Depends(get_db), trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        add_to_llmjob_table(response, db, trace_id)
        # print('abc')
        return await generate_email(response,trace_id)
    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = 500)

    
