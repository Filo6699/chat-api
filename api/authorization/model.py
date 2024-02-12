from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import UUID

from api.config import username_regex, password_regex


class AuthBase(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=32,
        pattern=username_regex,
        examples=["ultra_nagibator3000"],
    )


class AuthPost(AuthBase):
    password: str = Field(
        min_length=4,
        max_length=32,
        pattern=password_regex,
        examples=["password123"],
    )


class AuthResponse(AuthBase):
    user_id: UUID
    token: str
