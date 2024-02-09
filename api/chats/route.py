from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.types import UUID

from .service import ChatService
from .model import Chat, ChatPost
from api.users.model import User
from api.utils import get_current_user
from api.database import get_session

router = APIRouter()


@router.get("/chats")
async def get_chats(
    session: AsyncSession = Depends(get_session),
):
    try:
        print("chats")
        chats = await ChatService.get_all_chats(session)
        return chats
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.get("/chats/{chat_id}")
async def get_chat(
    chat_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        chats = await ChatService.get_chat(chat_id, session)
        return chats
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.post("/chats")
async def create_chat(
    chat: ChatPost,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        message = await ChatService.create_chat(user, chat, session)
        return message
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )


@router.delete("/chats/{chat_id}")
async def delete_chat(
    chat_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await ChatService.delete_chat(user, chat_id, session)
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=error.args[0],
        )
