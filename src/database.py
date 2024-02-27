from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()



engine = create_engine("mysql+pymysql://root:MANOsince%402003@localhost:3306/MSP_API",pool_size=10, max_overflow=20)

session_local = sessionmaker(autocommit=False,autoflush=False, bind=engine)

base = declarative_base()

