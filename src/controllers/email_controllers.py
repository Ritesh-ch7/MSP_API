from fastapi.responses import JSONResponse
from src.services.fewshot_service import few_shot_body_template
from src.services.noshot_service import no_shot_body_template
from src.services.no_shot_servicerequest import no_shot_service_body_template
from src.services.no_shot_incidentrequest import no_shot_incident_body_template
from src.services.no_shot_namelessrequest import no_shot_nameless_body_template

from src.schemas.users import *
import uuid, json
from src.config.logger_config import new_logger as logger
from src.utils.constants import *
from src.services.subject_service import subject_generator
from src.controllers.database_controllers.tasks_db.update_failed_reason import update_failed_reason
from src.controllers.database_controllers.tasks_db.update_response import update_task_response
from fastapi import HTTPException
from dotenv import load_dotenv
import os
from src.services.apikey_validation import check_openai_api_key



async def generate_email(response: any,db,llm_id, task_id, user_id, trace_id : str = None):

    """
    Generates an email based on the response from a language model for a given task.
 
    Args:
    - response: The response from the language model.
    - db: The database session to perform the database operations.
    - llm_id: The ID associated with the language model.
    - task_id: The ID of the task for which the email is generated.
    - user_id: The ID of the user generating the email.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.
 
    Returns:
    A JSON response containing the generated email subject, body, and associated IDs.
 
    Raises:
    HTTPException: If an error occurs during the email generation or database operation,
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        validated_item =  response["validated_item"]
        reference =  response["reference_list"]

        api_key = os.getenv('API_KEY')
        if(len(reference)==0):
            # no shot
            mail_subject = subject_generator(validated_item.ticket_id,validated_item.requestor_name,validated_item.title,validated_item.priority,validated_item.severity,trace_id)
            
            if validated_item.ticket_type=='Service Request':
                print(validated_item.status.value)
                mail_body =  no_shot_service_body_template(validated_item.ticket_id,validated_item.requestor_name,validated_item.title,validated_item.description,validated_item.priority,validated_item.severity,validated_item.ticket_type,validated_item.source,validated_item.status.value,trace_id)

            else:
                # mail_body =  no_shot_incident_body_template(validated_item.ticket_id,validated_item.company_name,validated_item.title,validated_item.description,validated_item.priority,validated_item.severity,validated_item.ticket_type, validated_item.status.value,trace_id)

                mail_body =  no_shot_nameless_body_template(validated_item.ticket_id,validated_item.title,validated_item.description,validated_item.priority,validated_item.severity,validated_item.ticket_type, validated_item.status.value,trace_id)



            

            mail_json_text = json.dumps({'subject':mail_subject, 'body' : mail_body})
            mail_json_form = json.loads(mail_json_text)
            await update_task_response(task_id, mail_json_form,db,user_id,trace_id)

            logger.debug(f"{trace_id}: Email has been generated successfully for the task {task_id}")
            return JSONResponse(content={
                "subject":mail_subject,
                "body": mail_body,
                "llm_id": llm_id
            }, status_code = OK)

        else: #Fewshot
            print("entered few shot")
            mail_subject = subject_generator(validated_item.ticket_id,validated_item.requestor_name,validated_item.description,validated_item.priority,validated_item.severity,trace_id)
            print("before few shot")
            mail_body =  few_shot_body_template(validated_item.ticket_id, validated_item.requestor_name, validated_item.priority, validated_item.severity, validated_item.description, reference, trace_id)
            print("after few shot")
            mail_json_text = json.dumps({'subject':mail_subject, 'body' : mail_body})
            mail_json_form = json.loads(mail_json_text)
            await update_task_response(task_id, mail_json_form,db,user_id,trace_id)

            logger.debug(f"{trace_id}: Email has been generated successfully for the task {task_id}")
            return JSONResponse(content={
                "subject":mail_subject,
                "body": mail_body,
                "llm_id": llm_id
            }, status_code = OK)

    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in LLM model mail generation: {str(e)}"
        await update_failed_reason(task_id, db, error_msg, trace_id)
        # print({e})
        raise HTTPException(status_code = INTERNAL_SERVER_ERROR, detail = f'{e}')
    

