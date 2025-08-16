from datetime import datetime
from sqlalchemy import BigInteger, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from bot.db import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime())
    username: Mapped[str | None]
    fullname: Mapped[str]
    language: Mapped[str] = mapped_column(String(5), default="ru")

    tg_premium: Mapped[bool]

    subscription_type: Mapped[str] = mapped_column(String(20), default="free")
    subscription_start: Mapped[datetime | None]
    subscription_end: Mapped[datetime | None]
    is_trial: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_provider: Mapped[str | None] = mapped_column(String(50))
    payment_id: Mapped[str | None] = mapped_column(String(100))