from typing import List
from sqlalchemy.orm import Session
from app.models import Questions
from app.common.logger import logger


class QuestionService:
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_all_questions(self) -> List[Questions]:
        """
        Get all questions from the database
        """
        try:
            questions = self.session.query(Questions).all()
            return questions
        except Exception as e:
            logger.error(f"Error getting all questions: {e}")
            raise e
