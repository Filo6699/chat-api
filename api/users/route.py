from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.types import UUID

from .service import UserService
from .model import User, UserPost, UserResponse, UserPostResponse
from api.utils import get_current_user
from api.database import get_session

router = APIRouter()


@router.get(
    "/users",
    response_model=List[UserResponse],
    tags=["users"],
)
async def get_users(
    session: AsyncSession = Depends(get_session),
):
    try:
        users = await UserService.get_all_users(session)
        return users
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        user = await UserService.get_user(user_id, session)
        return user
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.post(
    "/users",
    response_model=UserPostResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users", "authorization"],
)
async def create_user(
    user: UserPost,
    session: AsyncSession = Depends(get_session),
):
    try:
        message = await UserService.create_user(user, session)
        return message
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
)
async def delete_message(
    user_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await UserService.delete_user(user, user_id, session)
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )
