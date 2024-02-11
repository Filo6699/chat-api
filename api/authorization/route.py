from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.types import UUID

from .service import AuthService
from .model import AuthResponse, AuthPost
from api.utils import get_current_user
from api.database import get_session

router = APIRouter()


@router.post(
    "/auth",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    tags=["authorization", "users"],
)
async def authorize(
    user: AuthPost,
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await AuthService.authorize(user, session)
        return result
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )
