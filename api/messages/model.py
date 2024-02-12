import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from pydantic.types import UUID as PUUID

from api.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        Integer,
        index=True,
        primary_key=True,
        autoincrement=True,
    )
    chat_id = Column(UUID, ForeignKey("chats.id"), index=True)
    author_id = Column(UUID, ForeignKey("users.id"), index=True)
    author_username = Column(String)

    chat = relationship("Chat", back_populates="messages")
    author = relationship("User", back_populates="messages")

    content = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)


class MessageBase(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=1024,
        examples=["dead chat? xd lmao"],
    )


class MessagePost(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    chat_id: PUUID
    author_id: PUUID
    author_username: str = Field(
        examples=["ultra_nagibator3000"],
    )
    created_date: datetime
