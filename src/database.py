from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()



engine = create_engine("mysql+pymysql://root:password%404869@localhost:3306/msp_app")

session_local = sessionmaker(autocommit=False,autoflush=False, bind=engine)

base = declarative_base()

