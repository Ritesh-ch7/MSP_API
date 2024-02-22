from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv
import os, uuid
from src.config.logger_config import new_logger as logger

load_dotenv()
api_key = os.getenv("API_KEY")

llm1 = ChatOpenAI(openai_api_key=api_key, temperature=0.3)

def generate_subject_template(issue_id, issue_description, trace_id : str = None):
    if(trace_id == None):
        trace_id = str(uuid.uuid4())

    template_subject = "you have to generate a subject line for the acknowledgement email about ticket {issue_id} related to {issue_description}. Maybe a simple subject like: 'Support Ticket {issue_id}: {issue_description}'  "
   
    subject_prompt = ChatPromptTemplate.from_messages([("system", template_subject)])
 
    sub_message = subject_prompt.format_messages(issue_id=issue_id, issue_description=issue_description)
   
    out = llm1.predict_messages(sub_message)
    return out.content