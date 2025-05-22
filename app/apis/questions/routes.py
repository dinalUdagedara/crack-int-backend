from typing import List, Optional
from fastapi import APIRouter, HTTPException, Path, Response, status
from uuid import UUID
from app import models
from app.apis.questions.schemas import QuestionSchema, UpdateQuestionSchema
from app.apis.questions.service import QuestionService
from app.common.http_response import CommonResponse
from app.database import db_dependency
import logging
from app.schemas import QuestionBase


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


@router.put("/{question_id}",
            name="Update question by ID",
            status_code=status.HTTP_200_OK,
            response_model=CommonResponse[Optional[QuestionSchema]]
            )
async def update_question(
    response: Response,
    db: db_dependency,
    question_id: str,
    question_data: UpdateQuestionSchema
):
    try:
        question_service = QuestionService(db)
        updated_question = question_service.update_question(
            question_id, question_data)

        if not updated_question:
            raise HTTPException(status_code=404, detail="Question not found")

        payload = CommonResponse(
            message="Question updated successfully",
            success=True,
            payload=updated_question,
            meta=None
        )
        response.status_code = status.HTTP_200_OK
        return payload

    except HTTPException as http_err:
        payload = CommonResponse(
            success=False, message=str(http_err.detail), payload=None, meta=None
        )
        response.status_code = http_err.status_code
        return payload

    except Exception as err:
        logger.error(f"Unexpected error updating question: {err}")
        payload = CommonResponse(
            success=False, message="Internal Server Error", payload=None, meta=None
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return payload


@router.delete("/{question_id}",
               name="Delete question by ID",
               status_code=status.HTTP_200_OK,
               response_model=CommonResponse[Optional[str]]
               )
async def delete_question(
    response: Response,
    db: db_dependency,
    question_id: str
):
    try:
        question_service = QuestionService(db)
        deleted = question_service.delete_question(question_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Question not found")

        payload = CommonResponse(
            message="Question deleted successfully",
            success=True,
            payload=f"Question with ID {question_id} has been deleted.",
            meta=None
        )
        response.status_code = status.HTTP_200_OK
        return payload

    except HTTPException as http_err:
        payload = CommonResponse(
            success=False, message=str(http_err.detail), payload=None, meta=None
        )
        response.status_code = http_err.status_code
        return payload

    except Exception as err:
        logger.error(f"Unexpected error deleting question: {err}")
        payload = CommonResponse(
            success=False, message="Internal Server Error", payload=None, meta=None
        )
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return payload


@router.post("/",
             name="Create question with choices",
             status_code=status.HTTP_201_CREATED,
             response_model=CommonResponse[QuestionSchema])
async def create_question(
    question: QuestionBase,
    response: Response,
    db: db_dependency
):
    try:
        question_service = QuestionService(db)
        created_question = question_service.create_question(question)

        if not created_question:
            raise HTTPException(
                status_code=400, detail="Failed to create question")

        return CommonResponse(
            message="Question created successfully",
            success=True,
            payload=created_question,
            meta=None
        )

    except HTTPException as http_err:
        response.status_code = http_err.status_code
        return CommonResponse(
            success=False,
            message=str(http_err.detail),
            payload=None,
            meta=None
        )
