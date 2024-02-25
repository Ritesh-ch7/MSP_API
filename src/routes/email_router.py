from fastapi import APIRouter,Depends
import uuid
from src.controllers.email_controllers import generate_email
from src.services.validate_input import validate_input_data
from fastapi.responses import JSONResponse
from src.config.logger_config import new_logger as logger

router = APIRouter()

@router.post("/email")
async def user_data(response: any = Depends(validate_input_data),trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        return await generate_email(response,trace_id)
    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = 500)

    
