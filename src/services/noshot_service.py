from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain import PromptTemplate

from dotenv import load_dotenv
import os, uuid
from src.config.logger_config import new_logger as logger

load_dotenv()
api_key = os.getenv("API_KEY")

llm1 = ChatOpenAI(openai_api_key=api_key, temperature=0.3)


def no_shot_body_template(ticket_id,requestor_name,message,priority,severity,trace_id:str = None):
    if trace_id == None:
        trace_id = str(uuid.uuid4())
    try:
        # print(ticket_id,requestor_name,message,priority,severity)
        prompt="""Answer the question based on the context below. If the description of ticket provided in question cannot be answered or is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description'.
    
        Context: You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email for the ticket to requester showing that you are working on resolving the issue. The ticket has ticket id, requester name, priority, severity and the description associated for each ticket which will be provided in the question.
        
        Question: Write an acknowledgement email body for ticket with ticket id- {ticket_id} to the requester- {requestor_name} stating that you are working regarding the issue- {message}. The ticket's priority is {priority} and also the severity of the ticket is {severity} where 4 means high severity and 1 has low severity. If the requester's priority and severity is low, don't mention the priority and severity explicitly in the mail but if the priority and severity is high then stress in the mail that we are working really hard and its our topmost priority like that. Generate the mail body having content of around 5-6 lines.
        
        Answer:"""
    
        no_shot_template=PromptTemplate(
            input_variables=["ticket_id","requestor_name","message","priority","severity"],
            template=prompt
        )
        
        query=no_shot_template.format(ticket_id=ticket_id, requestor_name=requestor_name, message=message, priority=priority, severity=severity)
        res =  llm1.invoke(query)
        return res.content
    except Exception as e:
        return f"error in test : {e}"

    

    