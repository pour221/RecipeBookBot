from datetime import datetime
from sqlalchemy import select
from sqlalchemy.types import BigInteger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.session import async_session
from bot.db.models import User


async def add_user(session: AsyncSession, tg_id: BigInteger, user_name: str, fullname: str, tg_premium: bool):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id,
                             username=user_name,
                             fullname=fullname,
                             tg_premium=tg_premium,
                             created_at=datetime.utcnow(),
                             ))
        await session.commit()