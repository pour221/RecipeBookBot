from datetime import datetime
from typing import List
from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text

from bot.db.base import Base
from bot.db.models.recipes import Recipe


class Collection(Base):
    __tablename__ = "collections"

    collection_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    name: Mapped[str] = mapped_column(String(100))
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                 onupdate=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="collections")
    recipes: Mapped[List['Recipe']] = relationship(back_populates='collection')

