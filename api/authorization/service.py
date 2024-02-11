from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from pydantic.types import UUID
from bcrypt import hashpw

from .model import AuthResponse
from api.users.model import User, UserPost
from api.utils import generate_token, hash_password
from api.exceptions import PermissionError, AuthError


class AuthService:
    @staticmethod
    async def authorize(
        form_data: UserPost,
        session: AsyncSession,
    ) -> User:
        query = select(User).where(User.username == form_data.username)
        user: User = (await session.execute(query)).scalars().first()
        if not user:
            raise NoResultFound("User not found.")
        stored_hash = user.password_hash
        ok = hashpw(form_data.password.encode("utf-8"), stored_hash) == stored_hash
        if not ok:
            raise AuthError("Wrong password.")
        auth_token = generate_token(user.id)
        return AuthResponse(
            username=user.username,
            user_id=user.id,
            token=auth_token,
        )
