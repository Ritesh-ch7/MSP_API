from fastapi import FastAPI
from src.routes import email_router
from src.config.logger_config import new_logger as logger
from src.utils.constants import BASE_URL

from fastapi.middleware.cors import CORSMiddleware
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
logger.info("Starting email generator")
app.include_router(email_router.router, prefix = BASE_URL)