from fastapi.responses import JSONResponse
from src.services.fewshot_service import few_shot_body_template
from src.services.noshot_service import no_shot_body_template
from src.schemas.users import *
import uuid
from src.config.logger_config import new_logger as logger
from src.utils.constants import *

async def generate_email(response: any,llm_id, trace_id : str = None):
    """
    Generates an email body based on the response and sends it to the user.

    Args:
    - response (any): The response object containing information such as validated_item and reference_list.
    - llm_id: The ID of the associated LLM job for tracking purposes.
    - trace_id (str, optional): A unique identifier for tracing purposes. 
      If not provided, a new UUID will be generated.

    Returns:
    JSONResponse: A JSON response containing the generated email body and associated LLM ID.
                  If successful, returns a status code of 200 (OK); otherwise, returns 500 (Internal Server Error).

    Raises:
    Exception: If an error occurs during the email generation process, it is logged, and a 500 (Internal Server Error) response is returned.
    """
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        validated_item =  response["validated_item"]
        reference =  response["reference_list"]

        if(len(reference)==0):
            # no shot
            generated_mail =  no_shot_body_template(validated_item.ticket_id,validated_item.requestor_name,validated_item.description,validated_item.priority,validated_item.severity,trace_id)
            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "body": generated_mail,
                "llm_id": llm_id
            }, status_code = OK)

        else: #Fewshot
            generated_mail =  few_shot_body_template(validated_item.ticket_id, validated_item.requestor_name, validated_item.priority, validated_item.severity, validated_item.description, reference, trace_id)
            logger.info(f"{trace_id}: Response sent sucessfully")
            return JSONResponse(content={
                "body": generated_mail,
                "llm_id": llm_id
            }, status_code = OK)

    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = INTERNAL_SERVER_ERROR)
    

