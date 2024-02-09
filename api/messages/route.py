from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.types import UUID

from .service import MessageService
from .model import MessagePost
from api.utils import get_current_user
from api.database import get_session
from api.users.model import User

router = APIRouter()


@router.get("/chats/{chat_id}/messages")
async def get_messages(
    chat_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        messages = await MessageService.get_all_messages(chat_id, session)
        return messages
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.get("/chats/{chat_id}/messages/{message_id}")
async def get_message(
    chat_id: UUID,
    message_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        message = await MessageService.get_message(chat_id, message_id, session)
        return message
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.post("/chats/{chat_id}/messages")
async def create_message(
    chat_id: UUID,
    message: MessagePost,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        message = await MessageService.create_message(
            chat_id, user.id, message, session
        )
        return message
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.delete("/chats/{chat_id}/messages/{message_id}")
async def delete_message(
    chat_id: UUID,
    message_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await MessageService.delete_message(
            chat_id, user.id, message_id, session
        )
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )
