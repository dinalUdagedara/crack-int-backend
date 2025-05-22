from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://postgres:12345678@localhost:5432/crack-int'

# Create SQLAlchemy engine
engine = create_engine(URL_DATABASE)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session for FastAPI routes

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Type alias for FastAPI dependency injection for DB session
db_dependency = Annotated[Session, Depends(get_db)]

# Base class for ORM models to inherit from
Base = declarative_base()
