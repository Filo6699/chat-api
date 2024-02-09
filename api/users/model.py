import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from api.database import Base


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

    messages = relationship("Message", back_populates="author", cascade="all, delete")


class UserPost(BaseModel):
    username: str
