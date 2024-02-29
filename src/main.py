from fastapi import FastAPI
from src.routes import email_router
from src.config.logger_config import new_logger as logger
from src.utils.constants import BASE_URL
import sys

sys.dont_write_bytecode = True
app = FastAPI()
logger.info("Starting email generator")
app.include_router(email_router.router, prefix = BASE_URL)