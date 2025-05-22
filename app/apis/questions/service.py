from typing import List, Optional
from sqlalchemy.orm import Session
from app.apis.questions.schemas import QuestionSchema, UpdateQuestionSchema
from app.models import Questions
from app.common.logger import logger
from sqlalchemy import select
from app.schemas import QuestionBase
from app.models import Choices


class QuestionService:
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_all_questions(self) -> List[QuestionSchema]:
        """
        Get all questions from the database
        """
        try:
            questions = self.session.query(Questions).all()
            return questions
        except Exception as e:
            logger.error(f"Error getting all questions: {e}")
            raise e

    def get_question_by_id(self, id: str) -> Optional[QuestionSchema]:
        """
        Get Question by ID
        """

        try:
            question = self.session.query(Questions).where(
                Questions.id == id).first()
            return question

        except Exception as e:
            logger.error(f"Error getting question with id {id}: {e}")
            raise e

    def update_question(self, id: str, question_data: UpdateQuestionSchema) -> Optional[QuestionSchema]:
        """
        Update a question by ID with new data.
        """
        try:
            question = self.session.query(Questions).filter(
                Questions.id == id).first()
            if not question:
                logger.warning(f"Question with id {id} not found.")
                return None

            # Update fields
            for field, value in question_data.model_dump(exclude_unset=True).items():
                setattr(question, field, value)

            self.session.commit()
            self.session.refresh(question)

            return question

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error updating question with id {id}: {e}")
            raise e

    def delete_question(self, id: str) -> bool:
        """
        Delete a question by ID.
        """
        try:
            question = self.session.query(Questions).filter(
                Questions.id == id).first()
            if not question:
                logger.warning(f"Question with id {id} not found.")
                return False

            self.session.delete(question)
            self.session.commit()
            return True

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error deleting question with id {id}: {e}")
            raise e

    def create_question(self, question_data: QuestionBase) -> Optional[QuestionSchema]:
        """
        Create a new question with its choices.
        """
        try:
            # Create question
            question = Questions(question_text=question_data.question_text)
            self.session.add(question)
            self.session.commit()
            self.session.refresh(question)

            # Create associated choices
            for choice in question_data.choices:
                db_choice = Choices(
                    choice_text=choice.choice_text,
                    is_correct=choice.is_correct,
                    question_id=question.id
                )
                self.session.add(db_choice)

            self.session.commit()
            self.session.refresh(question)

            return question  # SQLAlchemy model; FastAPI will convert to response model

        except Exception as e:
            self.session.rollback()
            logger.error(f"Error creating question: {e}")
            raise e
