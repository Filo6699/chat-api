from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from pydantic.types import UUID
from bcrypt import hashpw

from .model import User, UserPost
from api.utils import generate_token, hash_password
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
            raise NoResultFound("User not found.")
        return user

    @staticmethod
    async def create_user(
        user: UserPost,
        session: AsyncSession,
    ) -> User:
        password_hash = hash_password(user.password)
        new_user = User(
            username=user.username,
            password_hash=password_hash,
            admin=False,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return {
            "id": new_user.id,
            "username": new_user.username,
            "admin": new_user.admin,
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
