from typing import List

from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from pydantic.types import UUID

from .model import Chat, ChatPost
from api.users.model import User
from api.database import get_session
from api.utils import convert_to_UUID
from api.exceptions import PermissionError


class ChatService:
    @staticmethod
    async def get_all_chats(
        session: AsyncSession,
    ) -> List[Chat]:
        query = select(Chat)
        return (await session.execute(query)).scalars().fetchall()

    @staticmethod
    async def get_chat(
        chat_id: UUID,
        session: AsyncSession,
    ) -> Chat:
        query = select(Chat).where(
            Chat.id == chat_id,
        )
        chat = (await session.execute(query)).scalars().first()
        if not chat:
            raise NoResultFound("chat not found")
        return chat

    @staticmethod
    async def create_chat(
        user: User,
        chat: ChatPost,
        session: AsyncSession,
    ) -> Chat:
        if user.admin == False:
            raise PermissionError()
        new_chat = Chat(
            name=chat.name,
        )
        session.add(new_chat)
        await session.commit()
        await session.refresh(new_chat)
        return new_chat

    @staticmethod
    async def delete_chat(
        user: User,
        chat_id: UUID,
        session: AsyncSession,
    ) -> None:
        if user.admin == False:
            raise PermissionError()
        chat = await ChatService.get_chat(chat_id, session)
        await session.delete(chat)
        await session.commit()
