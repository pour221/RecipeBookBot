from datetime import datetime
from typing import List
from sqlalchemy import BigInteger, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from bot.db.models import Collection
from .base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    created_at: Mapped[datetime] = mapped_column(DateTime())
    username: Mapped[str | None]
    fullname: Mapped[str | None]

    language: Mapped[str] = mapped_column(String(5), default="en")
    active_collection_id: Mapped[int | None] =  mapped_column(ForeignKey("collections.collection_id"), nullable=True)
    user_base_collection_id: Mapped[int | None] =  mapped_column(ForeignKey("collections.collection_id"), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_active_at: Mapped[datetime | None]

    tg_premium: Mapped[bool]

    subscription_type: Mapped[str] = mapped_column(String(20), default="free")
    subscription_start: Mapped[datetime | None]
    subscription_end: Mapped[datetime | None]
    is_trial: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_provider: Mapped[str | None] = mapped_column(String(50))
    payment_id: Mapped[str | None] = mapped_column(String(100))

    base_collection: Mapped[List["Collection"]] = relationship(
        back_populates='user',
        foreign_keys=[user_base_collection_id]
    )
    active_collection: Mapped[List["Collection"]] = relationship(
        back_populates='user',
        foreign_keys=[active_collection_id]

    )
    collections: Mapped[List["Collection"]] = relationship(
        back_populates="user",
        foreign_keys = 'Collection.user_id',
        cascade="all, delete-orphan")

    recipes: Mapped[List["Recipe"]] = relationship(
        back_populates='user',
        cascade="all, delete-orphan"
    )