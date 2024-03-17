import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.getenv('DSN'), pool_size=5, max_overflow=10, isolation_level="READ COMMITTED")
Session = sessionmaker(bind=engine, autoflush=False)
