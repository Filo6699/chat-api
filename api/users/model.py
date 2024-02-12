import uuid

from sqlalchemy import Column, String, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from pydantic.types import UUID as PUUID

from api.database import Base
from api.config import username_regex, password_regex


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    admin = Column(Boolean)
    username = Column(String, unique=True)
    password_hash = Column(LargeBinary)

    messages = relationship("Message", back_populates="author", cascade="all, delete")


class UserBase(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=32,
        pattern=username_regex,
        examples=["ultra_nagibator3000"],
    )


class UserPost(UserBase):
    password: str = Field(
        min_length=4,
        max_length=32,
        pattern=password_regex,
        examples=["password123"],
    )


class UserPostResponse(UserBase):
    id: PUUID
    token: str = Field(examples=["eyJhbGTiOiJIUzI1.eyJzdWIi.gnz-vjKL"])
    admin: bool


class UserResponse(UserBase):
    id: PUUID
    admin: bool
