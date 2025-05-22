from typing import List
from fastapi import APIRouter, HTTPException, Response, status
from app import models
from app.apis.questions.schemas import QuestionSchema
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
            response_model=CommonResponse[List[QuestionSchema]]
            )
async def read_question_from_service(response: Response, db: db_dependency):

    try:
        question_service = QuestionService(db)
        questions = question_service.get_all_questions()

        if not questions:
            raise HTTPException(status_code=404, detail='Question Not Found')

        payload = CommonResponse(
            message="Questions retrieved successfully",
            success=True,
            payload=questions,
            meta=None,
        )
        response.status_code = status.HTTP_200_OK
        return payload

    except HTTPException as http_err:
        payload = CommonResponse(
            success=False, message=str(http_err.detail), payload=None, meta=None
        )
        response.status_code = http_err.status_code
        return payload
