from fastapi.routing import APIRouter

from app.apis.questions.routes import router as questions_router

api_router = APIRouter()


api_router.include_router(
    questions_router, prefix="/questions", tags=["questions"])
