from typing import List

from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from pydantic.types import UUID

from .model import User, UserPost
from api.database import get_session
from api.utils import convert_to_UUID, generate_token
from api.exceptions import PermissionError


class UserService:
    @staticmethod
    async def get_all_users(
        session: AsyncSession,
    ) -> List[User]:
        query = select(User)
        return (await session.execute(query)).scalars().fetchall()

    @staticmethod
    async def get_user(
        user_id: UUID,
        session: AsyncSession,
    ) -> User:
        query = select(User).where(
            User.id == user_id,
        )
        user = (await session.execute(query)).scalars().first()
        if not user:
            raise NoResultFound("user not found")
        return user

    @staticmethod
    async def create_user(
        user: UserPost,
        session: AsyncSession,
    ) -> User:
        new_user = User(
            username=user.username,
            admin=False,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return {
            "id": new_user.id,
            "username": new_user.username,
            "token": generate_token(new_user.id),
        }

    @staticmethod
    async def delete_user(
        user: User,
        user_id: UUID,
        session: AsyncSession,
    ) -> None:
        if user.admin == False and user.id != user_id:
            raise PermissionError()
        del_user = await UserService.get_user(user_id, session)
        await session.delete(del_user)
        await session.commit()
