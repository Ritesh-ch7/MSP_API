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
 
llm1 = ChatOpenAI(openai_api_key=api_key, temperature=0.3)
 
 
def subject_generator(ticket_id,requestor_name,description,priority,severity,trace_id:str = None):

    """
    Generates an email subject using a template based on the provided input variables.
 
    Args:
    - ticket_id: The ID of the ticket associated with the email subject.
    - requestor_name: The name of the requester associated with the ticket.
    - description: The description of the ticket.
    - priority: The priority of the ticket.
    - severity: The severity of the ticket.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.
 
    Returns:
    The generated email subject.
 
    Raises:
    HTTPException: If an error occurs during the email subject generation,
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    
    if trace_id == None:
        trace_id = str(uuid.uuid4())
    try:

        no_shot_template=PromptTemplate(
            input_variables=["ticket_id","requestor_name","description","priority","severity"],
            template=SUBJECT_PROMPT
        )
       
        query=no_shot_template.format(ticket_id=ticket_id, requestor_name=requestor_name, description=description, priority=priority, severity=severity)
        res =  llm1.invoke(query)

        logger.debug(f'{trace_id} email subject has been generated')
        
        return res.content
    
    except Exception as e:
        logger.error(f'{trace_id} email subject cant be generated for{e}')
        raise HTTPException(status_code=INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}")
    