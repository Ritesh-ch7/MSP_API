from fastapi import Request, HTTPException
from src.utils.constants import *
from src.services.regenerate_service import regenerate_mail_template
from src.controllers.database_controllers.tasks_db.update_task_feedback import update_task_feedback
from fastapi.responses import JSONResponse
from src.controllers.database_controllers.tasks_db.update_response import update_task_response
from src.controllers.database_controllers.tasks_db.update_task_feedback import update_task_feedback
from src.controllers.database_controllers.tasks_db.tasks import add_task
from src.services.fetch_previous_mails import fetch_prev_mails
from src.controllers.database_controllers.tasks_db.update_status import update_task_status
from src.controllers.database_controllers.tasks_db.update_failed_reason import update_failed_reason
import uuid, json
from src.config.logger_config import new_logger as logger

async def regenerate_mail(request:Request,user_id, db, trace_id):

    """
    Regenerates an email based on the provided email body, subject, and language model ID.
 
    Args:
    - request: The FastAPI Request object containing the JSON body with 'body', 'subject', and 'llm_id'.
    - user_id: The ID of the user regenerating the email.
    - db: The database session to perform the database operations.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.
 
    Returns:
    A JSON response containing the regenerated email subject, body, and associated IDs.
 
    Raises:
    HTTPException: If an error occurs during the email regeneration or database operation,
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        task_id = ''
        request_data = await request.json()
        body = request_data.get('body',None)
        subject = request_data.get('subject',None)
        llm_id = request_data.get('llm_id',None)

        await update_task_feedback(llm_id, db, 'Negative', user_id, trace_id)
        task_id = add_task(llm_id,[], user_id, db, trace_id)

        
        if body and llm_id and subject:

            previous_mails = await fetch_prev_mails(llm_id, db, trace_id)

            if(len(previous_mails) == 0):
                logger.error(f'{trace_id} No previous mails with llm_id {llm_id} are present in the database')
                raise HTTPException(status_code = NOT_FOUND, message = f"No previous mails with llm_id {llm_id} are present in the database')")
            
            await update_task_status(task_id, db, 'InProgress', user_id, trace_id)
            
            regenerated_mail_body = regenerate_mail_template(previous_mails,llm_id)
            
            mail_json_text = json.dumps({'subject':subject, 'body' : regenerated_mail_body})
            mail_json_form = json.loads(mail_json_text)

            await update_task_response(task_id, mail_json_form,db,user_id,trace_id)
            logger.debug(f'{trace_id} email has been re-generated')

            await update_task_status(task_id, db, 'Completed', user_id, trace_id)
            return JSONResponse(content={
                "subject":subject,
                "body": regenerated_mail_body,
                "llm_id": llm_id
            }, status_code = OK)
        
        else:
            error_msg = f"body or llm_id is missing in request body"
            logger.error(f'{trace_id} body or llm_id is missing in request body')
            return JSONResponse(content={"message":error_msg},status_code = UNPROCESSABLE_ENTITY)

    except Exception as e:
        error_msg = f"Error in regenerate_mail : {e}"
        await update_failed_reason(task_id, db, error_msg, trace_id)
        logger.error(f'{trace_id} Error in mail regeneration : {e}')
        return JSONResponse(content={"message":error_msg},status_code = INTERNAL_SERVER_ERROR)
    
    