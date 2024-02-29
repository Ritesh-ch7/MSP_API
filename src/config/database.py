from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

db_key = os.getenv('DB_CONNECTION')
engine = create_engine(db_key,pool_size=10, max_overflow=20)

session_local = sessionmaker(autocommit=False,autoflush=False, bind=engine)

base = declarative_base()



