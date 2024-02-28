#status codes
OK = 200
CREATED = 201
ACCEPTED = 202
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
UNPROCESSABLE_ENTITY = 422
INTERNAL_SERVER_ERROR = 500

#paths
BASE_URL = "/api/v1"

#templates
SUBJECT_PROMPT="""
        Answer the question based on the context below. If the description of ticket provided in question cannot be answered or is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description'.
        Context: You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email body for the ticket to requester. The ticket has ticket id, requester name, priority, severity and the description associated for each ticket, which will be provided in the question.
        Question: You have to generate a subject line for the acknowledgement email about ticket {ticket_id} related to {description}. Maybe a simple subject like: 'Support Ticket ticket_id: description'  
        Answer:"""

NO_SHOT_PROMPT="""
        Answer the question based on the context below. If the description of ticket provided in question cannot be answered or is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description'.
        Context: You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email body for the ticket to requester showing that you are working on resolving the issue. The ticket has ticket id, requester name, priority, severity and the description associated for each ticket which will be provided in the question.
        Question: Write an acknowledgement email body for ticket with ticket id- {ticket_id} to the requester- {requestor_name} stating that you are working regarding the issue- {description}. The ticket's priority is {priority} and also the severity of the ticket is {severity} where 4 means high severity and 1 has low severity. If the requester's priority and severity is low, don't mention the priority and severity explicitly in the mail but if the priority and severity is high then stress in the mail that we are working really hard and its our topmost priority like that. Generate the mail body having content of around 5-6 lines. I only need the email body and not subject of the mail. Also, at the end after regards, I only want OSI Digital, I don't want name to be mentioned after regards. 
        Answer:"""

FEW_SHOT_PROMPT = """
        User: Write an acknowledgement email body for ticket with ticket id- {ticket_id} to the requester- {requester_name} stating that you are working regarding the issue- {description}. The ticket's priority is {priority} and also the severity of the ticket is {severity} where 4 means high severity and 1 has low severity. If the requester's priority and severity is low, don't mention the priority and severity explicitly in the mail but if the priority and severity is high then stress in the mail that we are working really hard and its our topmost priority like that. Generate the mail body having content of around 5-6 lines. I only need the email body and not subject of the mail. Also, at the end after regards, I only want OSI Digital, I don't want name to be mentioned after regards. 
        AI: {ref}
        """

FEW_SHOT_PREFIX = """
        You have to write a acknowledgement mail body, by taking the given example as reference. If the description of ticket provided in suffix cannot be answered or if it is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description' ."""
 

FEW_SHOT_SUFFIX = """
        User: Now generate a mail body which is almost similar to the above given examples and make sure the new mail generated is matching the current ticket details which is being provided now where the ticket id is-{ticket_id}, the requester name is -{requester_name}, the ticket description is- {description}. The ticket's priority is - {priority} and also the severity of the ticket is -{severity} where 4 means high severity and 1 has low severity. I only need the email body and not subject of the mail. Also, at the end after regards, I only want OSI Digital, I don't want name to be mentioned after regards. 
        AI: """

REGENERATE_PROMPT="""
        Answer the question based on the context below. 
        Context: You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email for the ticket to requester showing that you are working on resolving the issue.
        Question: You have provided me with the following emails already but the customer isn't satisfied with the email generated. the already sent emails are - {prev_emails}. Rewrite the previous email in a  different way, ensuring the same message is conveyed but with different wordings. I only need the email body and not subject of the mail. Also, at the end after regards, I only want OSI Digital, I don't want name to be mentioned after regards. 
        Answer:"""