import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DSN = os.getenv('DSN')

engine = create_engine(DSN, pool_size=5, max_overflow=10, isolation_level="READ COMMITTED")

Base = declarative_base()

Session = sessionmaker(bind=engine, autoflush=False)
