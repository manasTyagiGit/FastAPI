from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#URL is URL = 'postgresql://<username>:<password>@<URL>/<Database>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost/fastapi'

#Creating an engine for connections
engine = create_engine (SQLALCHEMY_DATABASE_URL)

#To interact with the DB, this is a session, with some default params
SessionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)

#The base class which is extended by other classes to create models for tables,
#this is imported in models.py
Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
