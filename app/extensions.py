import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

DSN = os.getenv('DATABASE_URI')

engine = create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)

