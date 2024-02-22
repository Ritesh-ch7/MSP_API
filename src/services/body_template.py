from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv
import os, uuid
from src.config.logger_config import new_logger as logger

load_dotenv()
api_key = os.getenv("API_KEY")

llm1 = ChatOpenAI(openai_api_key=api_key, temperature=0.3)

def generate_body_template(ticket_id, requester_name, priority, severity, text, trace_id : str = None):
    if (trace_id == None):
        trace_id = str(uuid.uuid4())

    template = "You are an L1 resource of our company 'OSI Digital' and have to write an acknowledgement email for the ticket {ticket_id} to {requester_name} stating you are working regarding the issue given by user which has {priority} as the ticket priority and has a severity of {severity} where 4 means high severity. write the mail in such a way that you show the customer that you are working to resolve the issue depending on the severity and priority but don't tell the user his/her priority and severity in the mail. If the user priority and severity is low, don't mention the priority and severity but if the priority and severity is high like if severity is 4 or priority is high then stress in the mail that we are working really hard and its our topmost priority add 1-2 lines like that to make it sound that we are equally concerned and will fix the issue as soon as possible. give the mail in  20 lines . After thank you, mention company name and i don't want any your_name field. I don't want best regards at the end, i only want thank you"
    human_template = "{text}"
 
    body_prompt = ChatPromptTemplate.from_messages([("system", template), ("human", human_template)])
 
    message_1 = body_prompt.format_messages(ticket_id=ticket_id, requester_name=requester_name, priority=priority, severity=severity, text=text)
   
    result = llm1.predict_messages(message_1)
    return result.content
