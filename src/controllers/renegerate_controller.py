from fastapi import Request
from src.utils.constants import *
from src.services.regenerate_service import regenerate_mail_template
from fastapi.responses import JSONResponse
import uuid

async def regenerate_mail(request:Request,trace_id):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        request_data = await request.json()
        body = request_data.get('body',None)
        subject = request_data.get('subject',None)
        llm_id = request_data.get('llm_id',None)
        if body and llm_id and subject:
            regenerated_mail_body = regenerate_mail_template(body,llm_id)
            return JSONResponse(content={
                "subject":subject,
                "body": regenerated_mail_body,
                "llm_id": llm_id
            }, status_code = OK)
        else:
            error_msg = f"body or llm_id is missing in request body"
            return JSONResponse(content={"message":error_msg},status_code = UNPROCESSABLE_ENTITY)

    except Exception as e:
        error_msg = f"Error in regenerate_mail : {e}"
        return JSONResponse(content={"message":error_msg},status_code = INTERNAL_SERVER_ERROR)