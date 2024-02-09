import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel, constr
from pydantic.types import UUID as PUUID

from api.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    chat_id = Column(UUID, ForeignKey("chats.id"), index=True)
    author_id = Column(UUID, ForeignKey("users.id"), index=True)
    author_username = Column(String)

    chat = relationship("Chat", back_populates="messages")
    author = relationship("User", back_populates="messages")

    content = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)


class MessageBase(BaseModel):
    content: constr(min_length=1, max_length=1024)


class MessagePost(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: PUUID
    chat_id: PUUID
    author_id: PUUID
    author_username: str
    created_date: datetime
