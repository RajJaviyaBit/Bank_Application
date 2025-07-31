from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

postgres_url = os.getenv("POSTGRES_URL")

def connect():
    """
    This functoin is for connecting postgres SQL Database and creating engine and connecting Session.
    These return session.    
    """
    engine = create_engine(postgres_url, echo =True)
    Session =sessionmaker(bind= engine)
    session = Session()
    return session