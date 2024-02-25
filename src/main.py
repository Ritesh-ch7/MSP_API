from fastapi import FastAPI,Depends
from fastapi.responses import JSONResponse
from src.routes import email_router
from src.services.validate_input import validate_input_data
from src.services.fewshot_service import few_shot_body_template
from src.services.noshot_service import no_shot_body_template
from src.config.logger_config import new_logger as logger
from src.controllers.email_controllers import generate_email
import uuid

app = FastAPI()

app.include_router(email_router.router, prefix="/api/v1")