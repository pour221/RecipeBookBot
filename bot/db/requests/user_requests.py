from datetime import datetime
from sqlalchemy import select
from sqlalchemy.types import BigInteger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.session import async_session
from bot.db.models import User, Collection


async def init_new_user(session: AsyncSession, tg_id: BigInteger, user_name: str, fullname: str, tg_premium: bool):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        user = User(tg_id=tg_id,
                             username=user_name,
                             fullname=fullname,
                             tg_premium=tg_premium,
                             created_at=datetime.utcnow(),
                             )
        session.add(user)
        await session.flush()

        collection = Collection(user_id=user.id, name='Base')
        session.add(collection)
        await session.flush()

        user.active_collection_id = collection.collection_id

        await session.commit()