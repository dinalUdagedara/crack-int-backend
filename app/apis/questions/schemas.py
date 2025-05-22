from typing import Optional
from pydantic import BaseModel

class QuestionSchema(BaseModel):
    id: int
    question_text: str

    class Config:
        orm_mode = True

class UpdateQuestionSchema(BaseModel):
    question_text: Optional[str] = None

    class Config:
        orm_mode = True