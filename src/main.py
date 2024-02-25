from fastapi import FastAPI
from src.routes import email_router

app = FastAPI()

app.include_router(email_router.router, prefix="/api/v1")