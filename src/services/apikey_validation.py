import openai
import os
import uuid
from src.config.logger_config import new_logger as logger
from fastapi import HTTPException
from src.utils.constants import *

def check_openai_api_key(openai_key, trace_id):
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
