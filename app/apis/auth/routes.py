from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, Request, Response, status
from app.apis.auth.service import AuthService
from app.database import db_dependency
from app.common.http_response import CommonResponse
from app.schemas import SocialProviderUserCreate

router = APIRouter()


@router.post(
    "/signup",
    name="Sign Up",
    status_code=status.HTTP_201_CREATED,
    response_model=CommonResponse
)
async def create_user(
    user: SocialProviderUserCreate,
    response: Response,
    db: db_dependency
):
    try:
        auth_service = AuthService(db)


        created_user = auth_service.createUser(user)

        if not created_user:
            raise HTTPException(
                status_code=400, detail="Failed to create user"
            )

        return CommonResponse(
            message="User created successfully",
            success=True,
            payload=created_user,
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
