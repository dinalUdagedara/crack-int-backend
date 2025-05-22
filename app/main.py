from typing import Annotated, List, Union
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app import models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    # change if using production frontend
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/questions/{question_id}')
async def read_question(question_id: int, db: db_dependency):
    result = db.query(models.Questions).filter(
        models.Questions.id == question_id).first()

    if not result:
        raise HTTPException(status_code=404, detail='Question Not Found')
    return result


@app.get('/choices/{question_id}')
async def read_choices(question_id: int, db: db_dependency):
    result = db.query(models.Choices).filter(
        models.Choices.question_id == question_id).all()

    if not result:
        raise HTTPException(status_code=404, detail='Choices Not Found')
    return result


@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)

        db.add(db_choice)

    db.commit()
