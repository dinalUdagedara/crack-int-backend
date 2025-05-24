"""
Database models for the Questions and Choices tables.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.database import Base


class Questions(Base):
    """
    Represents a question in the database.
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)


class Choices(Base):
    """
    Represents possible choices for a question.
    """
    __tablename__ = 'choices'

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'))


class User(Base):
    """
    Represents user created with a social provider login
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    # password = Column(String)
