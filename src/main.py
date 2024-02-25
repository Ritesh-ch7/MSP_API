from fastapi import FastAPI,Depends
from fastapi.responses import JSONResponse
from src.routes import email_router
from src.services.validate_input import validate_input_data
from src.services.fewshot_service import few_shot_body_template
from src.services.noshot_service import no_shot_body_template
from src.config.logger_config import new_logger as logger
import uuid

app = FastAPI()

# app.include_router(email_router.router, prefix="/api/v1")

@app.post("/email")
async def user_data(response: any = Depends(validate_input_data), trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    print("Here")
    try:
        validated_item = response["validated_item"]
        reference = response["reference_list"]

        if(len(reference)==0):
            # no shot
            generated_mail =  no_shot_body_template(validated_item.ticket_id,validated_item.requestor_name,validated_item.message,validated_item.priority,validated_item.severity,trace_id)
            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "subject": generated_mail
            }, status_code = 200)

        else: #Fewshot
            generated_mail =  few_shot_body_template(validated_item.ticket_id, validated_item.requestor_name, validated_item.priority, validated_item.severity, validated_item.message, reference, trace_id)
            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "subject": generated_mail
            }, status_code = 200)

    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = 500)