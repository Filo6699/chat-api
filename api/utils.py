from uuid import UUID

from jose import JWTError, jwt
from fastapi import Header, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from bcrypt import gensalt, hashpw

from api.config import ENCRYPTION_ALGORITHM, JWD_ENCRYPTION_KEY
from api.database import get_session
from api.users.model import User


def convert_to_UUID(uuid: str) -> UUID:
    try:
        return UUID(uuid)
    except ValueError:
        raise ValueError("Incorrect UUID format.")


def generate_token(user_id: UUID):
    payload = {
        "sub": str(user_id),
    }
    token = jwt.encode(payload, JWD_ENCRYPTION_KEY, algorithm=ENCRYPTION_ALGORITHM)
    return token


async def get_current_user(
    token: str = Header(...), session: AsyncSession = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWD_ENCRYPTION_KEY, algorithms=ENCRYPTION_ALGORITHM)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as err:
        raise credentials_exception
    query = select(User).where(
        User.id == user_id,
    )
    try:
        user = (await session.execute(query)).scalars().first()
    except:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user


def hash_password(password):
    salt = gensalt()
    return hashpw(password.encode("utf-8"), salt)
