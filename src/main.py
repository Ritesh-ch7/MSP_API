from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from src.schemas.users import *
from src.services.body_template import generate_body_template
from src.services.validate_input import validate_input_data
from src.services.subject_template import generate_subject_template
import uuid
from src.config.logger_config import new_logger as logger


app = FastAPI()

@app.post("/email/")
async def user_data(validated_item: any = Depends(validate_input_data), trace_id : str = None):
    if(not trace_id): trace_id = str(uuid.uuid4())
    if isinstance(validated_item,Ticket):
        try:
            sub_prompt =  generate_subject_template(validated_item.ticket_id, validated_item.message)
            body_prompt =  generate_body_template(validated_item.ticket_id, validated_item.requestor_name, validated_item.priority, validated_item.severity, validated_item.message)
            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "subject": sub_prompt,
                "body": body_prompt
            }, status_code = 200)

        except Exception as e:
            logger.error(f"{trace_id}: {e}")
            error_msg = f"Error in user_data function: {str(e)}"
            return JSONResponse(content={"message": error_msg}, status_code = 500)
    else:
        print("wrong")
        logger.error(f"{trace_id}: Validation Error of the request")
        return validated_item



