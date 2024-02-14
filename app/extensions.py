from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DSN = 'postgresql+psycopg2://max:4125@127.0.0.1:5431/flask_app_db'

engine = create_engine(DSN, echo=True, pool_size=5, max_overflow=10)

Base = declarative_base()

Session = sessionmaker(bind=engine, autoflush=False)