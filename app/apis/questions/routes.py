from fastapi import APIRouter, HTTPException, status
from app import models
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

    # logger.info(result)

    # return CommonResponse[List[QuestionBase]](
    #     message="Questions retrieved successfully",
    #     success=True,
    #     payload=result,
    #     meta=None  # Or you can calculate pagination info here
    # )
