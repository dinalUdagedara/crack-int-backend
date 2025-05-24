from typing import Optional
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.apis.auth.schemas import SocialProviderUser
from app.common.logger import logger
from sqlalchemy.orm import Session
from app.models import User

from app.schemas import SocialProviderUserCreate


class AuthService:
    """Service for authentication and user management operations"""

    def __init__(self, db_session: Session):
        self.session = db_session

    # def createUser(
    #     self,
    #     userData: SocialProviderUserCreate
    # ) -> Optional[SocialProviderUser]:

    #     user = User(
    #         first_name=userData.first_name,
    #         last_name=userData.last_name,
    #         email=userData.email
    #     )

    #     self.session.add(user)
    #     self.session.commit()
    #     self.session.refresh(user)

    #     return user

    def createUser(self, user_create: SocialProviderUserCreate) -> Optional[User] :
        existing_user = self.session.query(User).filter(
            User.email == user_create.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # new_user = User(**user_create.model_dump())

        new_user = User(
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            email=user_create.email
        )
        self.session.add(new_user)
        logger.info(f"New user created: {new_user}")

        try:
            self.session.commit()
            self.session.refresh(new_user)
            return new_user
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(
                status_code=500, detail="Failed to create user due to integrity error.")
