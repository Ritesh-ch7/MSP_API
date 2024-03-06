from fastapi import APIRouter,Depends, Request
from fastapi.responses import Response
import uuid
from src.controllers.email_controllers import generate_email
from src.services.validate_input import validate_input_data
from fastapi.responses import JSONResponse
from src.config.logger_config import new_logger as logger
from sqlalchemy.orm import Session
from src.controllers.database_controllers.llm_jobs_db.llmjob import add_to_llmjob_table
from src.controllers.database_controllers.tasks_db.tasks import add_task
from src.controllers.database_controllers.tasks_db.update_status import update_task_status
from src.controllers.database_controllers.tasks_db.update_failed_reason import update_failed_reason
from src.utils.constants import *
from src.config.get_db import get_db
from src.controllers.renegerate_controller import regenerate_mail
from fastapi import HTTPException
from src.models.tickets import TicketBase

router = APIRouter()



@router.post("/{user_id}/email")
async def user_data(user_id, request : Request, db :Session = Depends(get_db), trace_id : str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    
    try:
        response = await validate_input_data(request, trace_id)
        
    except Exception as e:
        logger.error(f"{trace_id}: {e}")
        error_msg = f"Error in user_data function: {str(e)}"
        return JSONResponse(content={"message": error_msg}, status_code = UNPROCESSABLE_ENTITY)
    
    try:
        llm_id =  add_to_llmjob_table(response['validated_item'], db, trace_id)
        task_id =  add_task(llm_id, response['reference_list'], user_id, db, trace_id)

    except Exception as e:
        logger.error(f'{trace_id} : {e}')
        return JSONResponse(content = {"message" : f'{str(e)}'})
    
    try:
        await update_task_status(task_id, db, 'Inprogress',user_id, trace_id)
        print('before')
        email_response = await generate_email(response,db,llm_id,task_id,user_id,trace_id)
        print(email_response)

        if(email_response.status_code < 400):
            logger.info("Email generated successfully")
            await update_task_status(task_id, db, 'Completed', user_id, trace_id)
            return email_response
    
    except Exception as e:
        await update_task_status(task_id, db, 'Failed', user_id, trace_id)
        await update_failed_reason(task_id,db,str({e}),trace_id)
        logger.error(f"{trace_id} : Task has been terminated {e}")
        return JSONResponse(content={"message": f'{str(e)}'}, status_code = INTERNAL_SERVER_ERROR)


@router.post("/{user_id}/regenerate")
async def regenerate(request : Request, user_id,  db :Session = Depends(get_db), trace_id:str = None):
    if(not trace_id):
        trace_id = str(uuid.uuid4())
    try:
        regenerated_mail = await regenerate_mail(request,user_id, db, trace_id)
        

        res = regenerated_mail.body.decode('utf-8')
        # res_with_newline=res.replace("\\n","\n")
        
        # email_with_newline = Response(content=res_with_newline, media_type="text/plain")

        logger.info(f'{trace_id} regenerated email has been sent successfully !!')

        return regenerated_mail
    
    except Exception as e:
        error_msg = f"Error in regenerate : main : {e}"
        
        return JSONResponse(content={"message":error_msg},status_code = INTERNAL_SERVER_ERROR)

    
@router.get("/tickets")
def fetch_all_records(db: Session = Depends(get_db)):
    records = db.query(TicketBase).all()
    return records
 
@router.get("/tickets/{id}")
def fetch_individual_record(id, db: Session = Depends(get_db)):
    record = db.query(TicketBase).filter(TicketBase.ticket_id == id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return record
