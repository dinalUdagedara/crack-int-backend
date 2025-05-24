from pydantic import BaseModel, EmailStr


class SocialProviderUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True
