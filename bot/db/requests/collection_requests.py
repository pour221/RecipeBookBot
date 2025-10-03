from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from bot.db.models import User, Collection, Recipe

async def create_new_collection(session: AsyncSession, user, collection_name):
    session.add(Collection(user_id=user.id,
                               name=collection_name))
    await session.commit()

async def get_collection_by_id(session, collection_id):
    collection = await session.scalar(select(Collection).where(Collection.collection_id == collection_id))
    return collection

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

async def set_active_collection(session: AsyncSession, user_id: int, collection_id: int):
    stmt = (update(User)
            .where(User.id == user_id)
            .values(active_collection_id=collection_id))
    await session.execute(stmt)
    await session.commit()

async def delete_collection(session: AsyncSession, user_id, requested_collection_id, base_collection_id):
    if requested_collection_id == base_collection_id:
        return False

    collection = await session.get(Collection, requested_collection_id)

    if collection and collection.user_id == user_id:
        await session.delete(collection)
        await session.commit()

        return True

    return False

async def rename_collection(session: AsyncSession, collection_id, user_id, new_name):
    stmt = (select(Collection)
            .where(Collection.collection_id == collection_id,
                   Collection.user_id == user_id))

    collection = await session.scalar(stmt)

    if not collection:
        return False

    collection.name = new_name
    await session.commit()
    return True
