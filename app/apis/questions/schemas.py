from pydantic import BaseModel

class QuestionSchema(BaseModel):
    id: int
    question_text: str

    class Config:
        orm_mode = True
