from datetime import datetime
from typing import List
from sqlalchemy import String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text, func

from .base import Base


class Collection(Base):
    __tablename__ = "collections"

    collection_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    name: Mapped[str] = mapped_column(String(100))
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="collections")
    recipes: Mapped[List['Recipe']] = relationship(back_populates='collection')

