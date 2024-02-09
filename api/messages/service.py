from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from pydantic.types import UUID

from .model import Message, MessagePost
from api.exceptions import PermissionError


class MessageService:
    @staticmethod
    async def get_all_messages(
        chat_id: UUID,
        session: AsyncSession,
    ) -> List[Message]:
        query = select(Message).where(Message.chat_id == chat_id)
        return (await session.execute(query)).scalars().fetchall()

    @staticmethod
    async def get_message(
        chat_id: UUID,
        message_id: UUID,
        session: AsyncSession,
    ) -> Message:
        query = select(Message).where(
            Message.chat_id == chat_id,
            Message.id == message_id,
        )
        message = (await session.execute(query)).scalars().first()
        if not message:
            raise NoResultFound("message not found")
        return message

    @staticmethod
    async def create_message(
        chat_id: UUID,
        author_id: UUID,
        message: MessagePost,
        session: AsyncSession,
    ) -> Message:
        new_message = Message(
            chat_id=chat_id,
            author_id=author_id,
            content=message.content,
        )
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)
        return new_message

    @staticmethod
    async def delete_message(
        chat_id: UUID,
        author_id: UUID,
        message_id: UUID,
        session: AsyncSession,
    ) -> None:
        message = await MessageService.get_message(chat_id, message_id, session)
        if message.author_id == author_id:
            await session.delete(message)
            await session.commit()
        else:
            raise PermissionError()
