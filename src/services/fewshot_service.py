from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain import FewShotPromptTemplate
from src.utils.constants import *
from fastapi import HTTPException
from dotenv import load_dotenv
import os, uuid
from src.config.logger_config import new_logger as logger
 
load_dotenv()
api_key = os.getenv("API_KEY")
 
llm1 = ChatOpenAI(openai_api_key=api_key, temperature=0.3)
 
def few_shot_body_template(ticket_id, requester_name, priority, severity, text, user_examples, trace_id : str = None):

    """
    Generates an email body using a few-shot learning template based on the provided input variables and user examples.
 
    Args:
    - ticket_id: The ID of the ticket associated with the email.
    - requester_name: The name of the requester associated with the ticket.
    - priority: The priority of the ticket.
    - severity: The severity of the ticket.
    - text: The text content of the email.
    - user_examples: A list of user-provided examples for few-shot learning.
    - trace_id: A unique identifier for tracing purposes. If not provided, a new UUID will be generated.
 
    Returns:
    The generated email body.
 
    Raises:
    HTTPException: If an error occurs during the email generation,
                   an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    
    if (trace_id == None):
        trace_id = str(uuid.uuid4())
 
    try:
        print("STAtRTEED")
        examples = user_examples
 
        example_prompt=PromptTemplate(
        input_variables=["ticket_id","requester_name","text","priority","severity","ref"],
        template = FEW_SHOT_PROMPT
        )
 
        few_shot_template=FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=FEW_SHOT_PREFIX,
        suffix=FEW_SHOT_SUFFIX,
        input_variables=["ticket_id","requester_name","text","priority","severity"]
        )
 
        logger.debug(f'{trace_id} email for few shot has been generated')
        query=few_shot_template.format(ticket_id=ticket_id, requester_name=requester_name, text=text, priority=priority, severity=severity, example=user_examples)

        return llm1.invoke(query).content
    
    except Exception as e:
        logger.error(f'{trace_id} email cant be generated {e}')
        raise HTTPException(status_code=INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}")
 
 