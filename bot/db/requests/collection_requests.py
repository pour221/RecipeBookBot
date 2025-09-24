from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from bot.db.models import User, Collection, Recipe, RecipeIngredient, Ingredient

async def create_new_collection(session: AsyncSession, user, collection_name):
    session.add(Collection(user_id=user.id,
                               name=collection_name))
    await session.commit()

async def get_collection_list_page(session: AsyncSession, user, page, page_size):
    collections_results = await session.scalars(select(Collection).where(Collection.user_id == user.id))
    all_collections = collections_results.all()

    stmt = (
        select(
            Collection,
            func.count(Recipe.recipe_id).label("recipes_count")
        )
        .outerjoin(Recipe, Recipe.collection_id == Collection.collection_id)
        .where(Collection.user_id == user.id)
        .group_by(Collection.collection_id)
        .limit(page_size + 1)
        .offset((page - 1) * page_size)
    )

    result = await session.execute(stmt)
    rows = result.all()
    collections_with_counts = [(row[0], row[1]) for row in rows]

    current_page_result = await session.scalars(select(Collection)
                                         .where(Collection.user_id == user.id)
                                         .limit(page_size+1)
                                         .offset((page-1)*page_size))
    current_page_collection = current_page_result.all()

    total_pages = (len(all_collections) + page_size - 1) // page_size
    has_next = len(current_page_collection) > page_size

    return collections_with_counts[:page_size], has_next, total_pages
