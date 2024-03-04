from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
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
 
def few_shot_body_template(ticket_id, requester_name, priority, severity, description, user_examples, trace_id : str = None):
    """
    Generates an email body using a few-shot prompt template.

    Args:
    - ticket_id: The ID of the ticket.
    - requester_name: The name of the ticket requester.
    - priority: The priority of the ticket.
    - severity: The severity of the ticket.
    - description: The description of the ticket.
    - user_examples: Examples provided by the user for few-shot learning.
    - trace_id (str, optional): A unique identifier for tracing purposes.
      If not provided, a new UUID will be generated.

    Returns:
    str: The generated email body based on the few-shot prompt template.

    Raises:
    HTTPException: If an error occurs during email generation, an HTTPException with status code 500 (Internal Server Error) is raised.
    """
    if (trace_id == None):
        trace_id = str(uuid.uuid4())
 
    try:
        examples = user_examples
 
        example_prompt=PromptTemplate(
        input_variables=["ticket_id","requester_name","description","priority","severity","ref"],
        template = FEW_SHOT_PROMPT
        )
 
        few_shot_template=FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=FEW_SHOT_PREFIX,
        suffix=FEW_SHOT_SUFFIX,
        input_variables=["ticket_id","requester_name","description","priority","severity"]
        )
 
        logger.debug(f'{trace_id} email for no shot has been generated')
        query=few_shot_template.format(ticket_id=ticket_id, requester_name=requester_name, description=description, priority=priority, severity=severity, example=user_examples)

        return llm1.invoke(query).content
    
    except Exception as e:
        logger.error(f'{trace_id} email cant be generated {e}')
        raise HTTPException(status_code=INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}")
 
 