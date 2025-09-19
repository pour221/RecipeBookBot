from sqlalchemy import func
from bot.db.models import User, Collection, Recipe, RecipeIngredient, Ingredient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def add_new_recipe(session: AsyncSession, user_id, name, description, ingredients_table, equipments, photos):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))
    session.add(Recipe(user_id=user.id,
                           collection_id=collection.collection_id,
                           recipe_name=name,
                           descriptions=description,
                           ingredients_table=ingredients_table,
                           equipments=equipments,
                           photos=photos
                           ))

    await session.commit()

async def quick_add_new_recipe(session: AsyncSession, user_id, name, description):
    await add_new_recipe(session,  user_id, name, description, None, None, None)

async def get_list_recipes(session: AsyncSession,  user_id):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))
    recipies = await session.scalars(select(Recipe).where(Recipe.collection_id == collection.collection_id))
    return recipies.all()

async def get_list_page(session: AsyncSession, user_id, page, page_size=20):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))

    total = await session.scalar(select(func.count()).select_from(Recipe).where(Recipe.user_id == user_id))

    stmt = (
            select(Recipe).where(Recipe.collection_id == collection.collection_id).limit(page_size+1).offset((page-1)*page_size)
        )
    results = await session.scalars(stmt)
    recipes = results.all()

    total_pages = max(1, (total + page_size - 1) // page_size)

    has_next = len(recipes) > page_size
    return recipes[:page_size], has_next, total_pages

async def get_recipe_by_number(session: AsyncSession, user_id: int, number: int) -> Recipe | None:
    # async with async_session() as session:
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))

    stmt = (
            select(Recipe)
            .where(Recipe.collection_id == collection.collection_id)
            .offset(number - 1)
            .limit(1)
        )
    result = await session.scalars(stmt)
    return result.first()