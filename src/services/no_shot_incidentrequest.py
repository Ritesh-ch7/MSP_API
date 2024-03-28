from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain import PromptTemplate
from src.utils.constants import *
from fastapi import HTTPException
from dotenv import load_dotenv
import os, uuid
from src.config.logger_config import new_logger as logger
 
load_dotenv()
api_key = os.getenv("API_KEY")
 
llm1 = ChatOpenAI(openai_api_key=api_key, temperature=0.1)

 
 
def no_shot_incident_body_template(ticket_id,company_name,title,description,priority,severity,ticket_type, status, sla, trace_id:str = None):

    """
    Generates an email body using a template for cases with no user-provided examples.
 
    Args:
    - ticket_id: The ID of the ticket associated with the email.
    - requestor_name: The name of the requester associated with the ticket.
    - description: The description of the ticket.
    - priority: The priority of the ticket.
    - severity: The severity of the ticket.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.
 
    Returns:
    The generated email body.
 
    Raises:
    HTTPException: If an error occurs during the email generation,
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """

    
    if trace_id == None:
        trace_id = str(uuid.uuid4())
    try:



        no_shot_template=PromptTemplate(
            input_variables=["ticket_id","company_name","title","description","priority","severity","ticket_type", "status", "sla"],
            template=NO_SHOT_PROMPT_incident
        )
       




        query=no_shot_template.format(ticket_id=ticket_id, company_name=company_name, title=title,description=description, priority=priority, severity=severity, ticket_type=ticket_type, status=status, sla=sla)
        res =  llm1.invoke(query)

        logger.debug(f'{trace_id} email for no shot has been generated')
        return res.content
    
    except Exception as e:
        logger.error(f'{trace_id} email cant be generated {e}')
        raise HTTPException(status_code=INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}")
    