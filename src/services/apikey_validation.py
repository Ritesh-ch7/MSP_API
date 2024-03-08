import openai
import os
import uuid
from src.config.logger_config import new_logger as logger
from fastapi import HTTPException
from src.utils.constants import *

def check_openai_api_key(openai_key, trace_id):

    """
    Verifies the validity of an OpenAI API key.
 
    Parameters:
    - openai_key (str): The OpenAI API key to be checked.
    - trace_id (str, optional): A unique identifier for tracing purposes. If not provided, a new one is generated.
 
    Returns:
    - str: The validated OpenAI API key.
 
    Raises:
    - HTTPException: If the OpenAI API key is expired (403) or invalid (401).
    """

    if not trace_id:
        trace_id = str(uuid.uuid4())
    openai.api_key = openai_key
    try:
        openai.Completion.create(model="gpt-turbo-3.5", prompt="This is a test", max_tokens=5)

    except openai.OpenAIError as e:
        error_message = str(e)
        if "expired" in error_message:
            logger.error(f'{trace_id} The OpenAI API key is expired: {error_message}')
            raise HTTPException(detail="The OpenAI API key has expired", status_code=403)
        else:
            logger.error(f'{trace_id} The OpenAI API key is invalid: {error_message}')
            raise HTTPException(detail="The provided OpenAI API key is not valid", status_code=401)
    return openai_key
