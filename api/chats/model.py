import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from pydantic.types import UUID as PUUID

from api.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    messages = relationship("Message", back_populates="chat", cascade="all, delete")

    name = Column(String)


class ChatPost(BaseModel):
    name: str
