from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain import PromptTemplate
from langchain import FewShotPromptTemplate

from dotenv import load_dotenv
import os, uuid
from src.config.logger_config import new_logger as logger

load_dotenv()
api_key = os.getenv("API_KEY")

llm1 = ChatOpenAI(openai_api_key=api_key, temperature=0.3)

def few_shot_body_template(ticket_id, requester_name, priority, severity, text, user_examples, trace_id : str = None):
    if (trace_id == None):
        trace_id = str(uuid.uuid4())

    try:

    
        examples = user_examples

        example_template="""
        User: Write an acknowledgement email body for ticket with ticket id- {ticket_id} to the requester- {requester_name} stating that you are working regarding the issue- {text}. The ticket's priority is {priority} and also the severity of the ticket is {severity} where 4 means high severity and 1 has low severity. If the requester's priority and severity is low, don't mention the priority and severity explicitly in the mail but if the priority and severity is high then stress in the mail that we are working really hard and its our topmost priority like that. Generate the mail body having content of around 5-6 lines. 
        AI: {ref}
        """


        example_prompt=PromptTemplate(
        input_variables=["ticket_id","requester_name","text","priority","severity","ref"],
        template=example_template
        )

        prefix=""" 
        You have to write a acknowledgement mail body, by taking the given example as reference. If the description of ticket provided in suffix cannot be answered or if it is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description' ."""


        suffix=""" 
        User: Now generate a mail body which is almost similar to the above given examples and make sure the new mail generated is matching the current ticket details which is being provided now where the ticket id is-{ticket_id}, the requester name is -{requester_name}, the ticket description is- {text}. The ticket's priority is - {priority} and also the severity of the ticket is -{severity} where 4 means high severity and 1 has low severity.
        AI: """


        few_shot_template=FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["ticket_id","requester_name","text","priority","severity"]
        )


        query=few_shot_template.format(ticket_id=ticket_id, requester_name=requester_name, text=text, priority=priority, severity=severity, example=user_examples)


        return llm1.invoke(query).content
    except Exception as e:
        return f"error in test : {e}"