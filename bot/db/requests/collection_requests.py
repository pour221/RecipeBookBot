from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.session import async_session
from bot.db.models import User, Collection, Recipe, RecipeIngredient, Ingredient

async def init_first_collection(session: AsyncSession, user_id):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))

    if not collection:
        session.add(Collection(user_id=user.id,
                                   name='Base'))
        await session.commit()

async def create_new_collection(session: AsyncSession, user_id, collection_name):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    session.add(Collection(user_id=user.id,
                               name=collection_name))
