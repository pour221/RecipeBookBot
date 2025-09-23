from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, Collection, Recipe, RecipeIngredient, Ingredient

# async def init_first_collection(session: AsyncSession, user_id):
#     user = await session.scalar(select(User).where(User.tg_id == user_id))
#     collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))
#
#     if not collection:
#         new_collection = Collection(user_id=user.id, name='Base')
#
#         session.add(new_collection)
#         await session.flush()
#
#         user.active_collection_id = new_collection.collection_id
#         await session.commit()

async def create_new_collection(session: AsyncSession, user, collection_name):
    session.add(Collection(user_id=user.id,
                               name=collection_name))
    await session.commit()
