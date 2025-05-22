from fastapi import APIRouter, HTTPException, status
from app import models
from app.apis.questions.service import QuestionService
from app.common.http_response import CommonResponse
from app.database import db_dependency
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/",
            name="Get all the questions",
            status_code=status.HTTP_200_OK,
            # response_model=CommonResponse,
            )
async def read_question(db: db_dependency):
    result = db.query(models.Questions).all()

    if not result:
        raise HTTPException(status_code=404, detail='Question Not Found')
    return result


@router.get("/from-service/",
            name="Get all the questions using the service function",
            status_code=status.HTTP_200_OK,
            )
async def read_question_from_service(db: db_dependency):

    question_service = QuestionService(db)
    questions = question_service.get_all_questions()
    if not questions:
        raise HTTPException(status_code=404, detail='Question Not Found')
    return questions
