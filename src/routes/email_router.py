from fastapi import APIRouter,Depends
import uuid
from src.controllers.email_controllers import generate_email
from src.services.validate_input import validate_input_data
from src.services.fewshot_service import few_shot_body_template
from src.services.noshot_service import no_shot_body_template
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/email")
async def user_data(response: any = Depends(validate_input_data), trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    print("Here")
    try:
        validated_item = response["validated_item"]
        reference = response["reference_list"]

        if(len(reference)==0):
            # no shot
            generated_mail =  few_shot_body_template(validated_item.ticket_id,validated_item.requestor_name,validated_item.message,validated_item.priority,validated_item.severity)
            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "subject": generated_mail
            }, status_code = 200)

        else: #Fewshot
            generated_mail =  no_shot_body_template(validated_item.ticket_id,validated_item.requestor_name,validated_item.message,validated_item.priority,validated_item.severity)
            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "subject": generated_mail
            }, status_code = 200)

    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = 500)

    
