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

NO_SHOT_PROMPT_service="""
        **Prompt:**

        Answer the question based on the context below.

        **Context:**

        You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email body for a ticket.

        * **Requester Name:** {requestor_name} 
        * **Ticket ID:** {ticket_id}
        * **Ticket Title:** {title}
        * **Description:** {description}
        * **Status:** {status} (e.g., Open, Pending) (if the status is closed then mention that the ticket has been resolved thank you. Our team took utmost care and resolved it at earliest possible, etc. Don't include lines like- We are actively working on a solution and expect to provide a quick update soon. )
        * **Ticket Type:** {ticket_type} service request
        * **Source:** {source} ( e.g., phone, email)
        * **Severity:** {severity} (1 is low severity and 4 is high severity)
        * **Priority:** {priority} (if priority is low the give acknowledgement mail in simple saying we are working, etc.)

        * Donot mention the priority and severity of the ticket explicitly in the mail.

        **Question:**

        Write an acknowledgement email body for the ticket. 

        * **Addressing:**
            * Use "Dear {requestor_name}," for service requests.
            
        * **Content:**
        * **Make sure the mail generated has nearly the lines mentioned beside the priority and severity combination.
            * Briefly acknowledge the issue ({title}).
            * State that the ticket has been {status}.
            * Craft the urgency based on a combination of priority (not revealed) and severity (not revealed):
                * **High Priority + Severity = 3 or 4:** (4 lines)
                    * Emphasize the importance of the issue and that the team is giving it utmost attention.
                    * Mention they are actively working on a solution and expect to provide a quick update.
                * **High Priority + Severity = 1 or 2:** (4 lines)
                    * Acknowledge the importance and that the team is working on a resolution.
                * **Medium Priority + Severity = 3 or 4:** (3 lines)
                    * Mention they are actively working on a solution and expect to provide a quick update.
                * **Medium Priority + Severity = 1 or 2:** (3 lines)
                    * Acknowledge the importance and that the team is working on a resolution. 
                * **Low Priority + Severity = 3 or 4:** (2 lines)
                    * Acknowledge the request's importance and that they are working diligently to address it.
                * **Low Priority + Severity = 1 or 2:** (2 lines)
                    * Confirm receipt of the ticket and that they are working to resolve it.
            * Donot mention the priority and severity of the ticket explicitly in the mail.
            * In case of Incident tickets donot mention we have received your request or thank you for reaching us out etc.
            * Make sure the mail generated has nearly the lines mentioned above.
        * **Closing:**
            * Use "Regards," or "Sincerely,"
            * Sign off with "OSI Digital" only (no name).

        Answer:"""


NO_SHOT_PROMPT_incident="""
        **Prompt:**

        Answer the question based on the context below.

        **Context:**

        You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email body for a ticket.
        
        * **Company Name:** {company_name} (use for incident requests like, dear company name,...)
        * **Ticket ID:** {ticket_id}
        * **Ticket Title:** {title}
        * **Description:** {description}
        * **Status:** {status} (e.g., Open, Pending)  (if the status is closed then mention that the ticket has been resolved thank you. Our team took utmost care and resolved it at earliest possible, etc. Don't include lines like- We are actively working on a solution and expect to provide a quick update soon. )
        * **Ticket Type:** {ticket_type} (incident)
        * **Severity:** {severity} (1 is low severity and 4 is high severity)
        * **Priority:** {priority} (if priority is low the give acknowledgement mail in simple saying we are working, etc.)

        * Donot mention the priority and severity of the ticket explicitly in the mail.

        **Question:**

        Write an acknowledgement email body for the ticket. 

        * **Addressing:**
            * Use "Dear {company_name}," for incident requests.
        * **Content:**
        * ** Donot include lines like 'thank you for reaching out, etc. Simply mention that We have received your ticket and team is working.
        * **Make sure the mail generated has nearly the lines mentioned beside the priority and severity combination.
            * Briefly acknowledge the issue ({title}).
            * State that the ticket has been {status}.
            * Craft the urgency based on a combination of priority (not revealed) and severity (not revealed):
                * **High Priority + Severity = 3 or 4:** (4 lines)
                    * Emphasize the importance of the issue and that the team is giving it utmost attention.
                    * Mention they are actively working on a solution and expect to provide a quick update.
                * **High Priority + Severity = 1 or 2:** (4 lines)
                    * Acknowledge the importance and that the team is working on a resolution.
                * **Medium Priority + Severity = 3 or 4:** (3 lines)
                    * Mention they are actively working on a solution and expect to provide a quick update.
                * **Medium Priority + Severity = 1 or 2:** (3 lines)
                    * Acknowledge the importance and that the team is working on a resolution. 
                * **Low Priority + Severity = 3 or 4:** (2 lines)
                    * Acknowledge the request's importance and that they are working diligently to address it.
                * **Low Priority + Severity = 1 or 2:** (2 lines)
                    * Confirm receipt of the ticket and that they are working to resolve it.
            * Donot mention the priority and severity of the ticket explicitly in the mail.
            * In case of Incident tickets donot mention we have received your request or thank you for reaching us out etc.
            * Make sure the mail generated has nearly the lines mentioned above.
        * **Closing:**
            * Use "Regards," or "Sincerely,"
            * Sign off with "OSI Digital" only (no name).

        Answer:"""


NO_SHOT_PROMPT="""
        Answer the question based on the context below. If the description of ticket provided in question cannot be answered or is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description'.
        Context: You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email body for the ticket to requester showing that you are working on resolving the issue. The ticket has ticket id, requester name, priority, severity and the description associated for each ticket which will be provided in the question.
        Question: Write an acknowledgement email body for ticket with ticket id- {ticket_id} to the requester- {requestor_name} stating that you are working regarding the issue- {description}. The ticket's priority is {priority} and also the severity of the ticket is {severity} where 4 means high severity and 1 has low severity. If the requester's priority and severity is low, don't mention the priority and severity explicitly in the mail but if the priority and severity is high then stress in the mail that we are working really hard and its our topmost priority like that. Generate the mail body having content of around 5-6 lines. I only need the email body and not subject of the mail. Also, at the end after regards, I only want OSI Digital, I don't want name to be mentioned after regards. 
        Answer:"""

FEW_SHOT_PROMPT = """
        User: Write an acknowledgement email body for ticket with ticket id- {ticket_id} to the requester- {requester_name} stating that you are working regarding the issue- {text}. The ticket's priority is {priority} and also the severity of the ticket is {severity} where 4 means high severity and 1 has low severity. If the requester's priority and severity is low, don't mention the priority and severity explicitly in the mail but if the priority and severity is high then stress in the mail that we are working really hard and its our topmost priority like that. Generate the mail body having content of around 5-6 lines. I only need the email body and not subject of the mail. Also, at the end after regards, I only want OSI Digital, I don't want name to be mentioned after regards. 
        AI: {ref}
        """

FEW_SHOT_PREFIX = """
        You have to write a acknowledgement mail body, by taking the given example as reference. If the description of ticket provided in suffix cannot be answered or if it is out of context like "tell me a joke", "how are you", etc., then provide the answer with 'I don't know, kindly give me a detailed ticket description' ."""
 

FEW_SHOT_SUFFIX = """
        User: Now generate a mail body which is almost similar to the above given examples and make sure the new mail generated is matching the current ticket details which is being provided now where the ticket id is-{ticket_id}, the requester name is -{requester_name}, the ticket description is- {text}. The ticket's priority is - {priority} and also the severity of the ticket is -{severity} where 4 means high severity and 1 has low severity. I only need the email body and not subject of the mail. Also, at the end after regards, I only want OSI Digital, I don't want name to be mentioned after regards. 
        AI: """

REGENERATE_PROMPT="""
        Answer the question based on the context below. 
        Context: You are an L1 resource of our company 'OSI Digital' and you have to write an acknowledgement email for the ticket to requester showing that you are working on resolving the issue.
        Question: You have provided me with the following emails already but the customer isn't satisfied with the email generated. the already sent emails are - {prev_emails}. Rewrite the previous email in a  different way, ensuring the same message is conveyed but with different wordings. I only need the email body and not subject of the mail. Also, at the end after regards, I only want OSI Digital, I don't want name to be mentioned after regards. 
        Answer:"""