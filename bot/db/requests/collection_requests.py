from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, Collection, Recipe, RecipeIngredient, Ingredient

async def create_new_collection(session: AsyncSession, user, collection_name):
    session.add(Collection(user_id=user.id,
                               name=collection_name))
    await session.commit()

async def get_collection_list_page(session: AsyncSession, user, page, page_size):
    collections_results = await session.scalars(select(Collection).where(Collection.user_id == user.id))
    all_collections = collections_results.all()

    current_page_result = await session.scalars(select(Collection)
                                         .where(Collection.user_id == user.id)
                                         .limit(page_size+1)
                                         .offset((page-1)*page_size))
    current_page_collection = current_page_result.all()

    total_pages = (len(all_collections) + page_size - 1) // page_size
    has_next = len(current_page_collection) > page_size

    return current_page_collection[:page_size], has_next, total_pages
