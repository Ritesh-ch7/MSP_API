from fastapi import FastAPI
from src.routes import email_router
from src.config.logger_config import new_logger as logger
from src.constants import BASE_URL

app = FastAPI()
logger.info("Starting email generator")
app.include_router(email_router.router, prefix = BASE_URL)