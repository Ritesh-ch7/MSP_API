#status codes
OK = 200
CREATED = 201
ACCEPTED = 202
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
INTERNAL_SERVER_ERROR = 500

#paths
BASE_URL = "/api/v1"

#templates
NO_SHOT_PROMPT="""Answer the question based on the context below. If the description of ticket provided in question cannot be answered or is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description'.
   
        Context: You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email for the ticket to requester showing that you are working on resolving the issue. The ticket has ticket id, requester name, priority, severity and the description associated for each ticket which will be provided in the question.
       
        Question: Write an acknowledgement email body for ticket with ticket id- {ticket_id} to the requester- {requestor_name} stating that you are working regarding the issue- {message}. The ticket's priority is {priority} and also the severity of the ticket is {severity} where 4 means high severity and 1 has low severity. If the requester's priority and severity is low, don't mention the priority and severity explicitly in the mail but if the priority and severity is high then stress in the mail that we are working really hard and its our topmost priority like that. Generate the mail body having content of around 5-6 lines.
       
        Answer:"""

FEW_SHOT_TEMPLATE = """
        User: Write an acknowledgement email body for ticket with ticket id- {ticket_id} to the requester- {requester_name} stating that you are working regarding the issue- {text}. The ticket's priority is {priority} and also the severity of the ticket is {severity} where 4 means high severity and 1 has low severity. If the requester's priority and severity is low, don't mention the priority and severity explicitly in the mail but if the priority and severity is high then stress in the mail that we are working really hard and its our topmost priority like that. Generate the mail body having content of around 5-6 lines.
        AI: {ref}
        """

FEW_SHOT_PREFIX = """
        You have to write a acknowledgement mail body, by taking the given example as reference. If the description of ticket provided in suffix cannot be answered or if it is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description' ."""
 

FEW_SHOT_SUFFIX = """
        User: Now generate a mail body which is almost similar to the above given examples and make sure the new mail generated is matching the current ticket details which is being provided now where the ticket id is-{ticket_id}, the requester name is -{requester_name}, the ticket description is- {text}. The ticket's priority is - {priority} and also the severity of the ticket is -{severity} where 4 means high severity and 1 has low severity.
        AI: """