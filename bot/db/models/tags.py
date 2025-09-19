from datetime import datetime
from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text

from .base import Base

class Tag(Base):
    __tablename__ = 'tags'

    tag_id: Mapped[int]
    name: Mapped[str] = mapped_column(String(50))

