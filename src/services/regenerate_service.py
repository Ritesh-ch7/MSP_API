from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain import PromptTemplate
from fastapi.responses import JSONResponse
from src.utils.constants import *
from fastapi import HTTPException
from dotenv import load_dotenv
import os, uuid
from src.config.logger_config import new_logger as logger
 
load_dotenv()
api_key = os.getenv("API_KEY")
 
llm1 = ChatOpenAI(openai_api_key=api_key, temperature=0.3)
 
def regenerate_mail_template(prev_emails,trace_id:str = None):
    if trace_id == None:
        trace_id = str(uuid.uuid4())
    try:
 
        regenerate_template=PromptTemplate(
            input_variables=["prev_emails"],
            template=REGENERATE_PROMPT
        )
 
        query = regenerate_template.format(prev_emails=prev_emails)
        res =  llm1.invoke(query)
        logger.debug(f'{trace_id} email has been re-generated')
        return res.content
       
   
    except Exception as e:
        logger.error(f'{trace_id} email cant be generated {e}')
        raise HTTPException(status_code=INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {str(e)}")