from datetime import datetime
from typing import List
from sqlalchemy import BigInteger, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    created_at: Mapped[datetime] = mapped_column(DateTime())
    username: Mapped[str | None]
    fullname: Mapped[str | None]
    language: Mapped[str] = mapped_column(String(5), default="ru")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_active_at: Mapped[datetime | None]

    tg_premium: Mapped[bool]

    subscription_type: Mapped[str] = mapped_column(String(20), default="free")
    subscription_start: Mapped[datetime | None]
    subscription_end: Mapped[datetime | None]
    is_trial: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_provider: Mapped[str | None] = mapped_column(String(50))
    payment_id: Mapped[str | None] = mapped_column(String(100))

    collections: Mapped[List["Collection"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan")

    recipes: Mapped[List["Recipe"]] = relationship(
        back_populates='user',
        cascade="all, delete-orphan"
    )