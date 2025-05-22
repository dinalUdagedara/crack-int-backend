from typing import List, Optional
from fastapi import APIRouter, HTTPException, Path, Response, status
from uuid import UUID
from app import models
from app.apis.questions.schemas import QuestionSchema
from app.apis.questions.service import QuestionService
from app.common.http_response import CommonResponse
from app.database import db_dependency
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/",
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


@router.get("/{question_id}",
            name="Get question by id",
            status_code=status.HTTP_200_OK,
            response_model=CommonResponse[Optional[QuestionSchema]]
            )
async def read_question_from_service(
    response: Response,
    db: db_dependency,
    # question_id: UUID = Path(..., description="The ID of the role to retrieve"),
    question_id: str

):

    try:
        question_service = QuestionService(db)
        questions = question_service.get_question_by_id(question_id)

        if not questions:
            raise HTTPException(status_code=404, detail='Question Not Found')

        payload = CommonResponse(
            message="Question retrieved successfully",
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
