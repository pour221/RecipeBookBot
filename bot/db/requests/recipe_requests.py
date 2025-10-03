from bot.db.models import Recipe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def add_new_recipe(session: AsyncSession, user, name,
                         collection_id, description, ingredients_table,
                         equipments, photos):
    session.add(Recipe(user_id=user.id,
                           collection_id=collection_id,
                           recipe_name=name,
                           descriptions=description,
                           ingredients_table=ingredients_table,
                           equipments=equipments,
                           photos=photos
                           ))

    await session.commit()

async def quick_add_new_recipe(session: AsyncSession, user, collection, name, description):
    await add_new_recipe(session,  user, name, collection, description, None, None, None)

async def get_list_page(session: AsyncSession, collection_id, page, page_size):
    total = await session.scalars(select(Recipe).where(Recipe.collection_id == collection_id))

    stmt = (
            select(Recipe)
            .where(Recipe.collection_id == collection_id)
            .limit(page_size+1)
            .offset((page-1)*page_size)
        )

    results = await session.scalars(stmt)
    recipes = results.all()

    total_pages = (len(total.all()) + page_size - 1) // page_size

    has_next = len(recipes) > page_size
    return recipes[:page_size], has_next, total_pages

async def get_recipe_by_id(session: AsyncSession, recipe_id):
    return await session.get(Recipe, recipe_id)

async def delete_recipe_by_id(session: AsyncSession, recipe):
    await session.delete(recipe)
    await session.commit()

async def update_recipe(session: AsyncSession, recipe_id: int, **kwargs):
    recipe = await session.scalar(select(Recipe).where(Recipe.recipe_id == recipe_id))

    if not recipe:
        return None

    for key, value in kwargs.items():
        if hasattr(recipe, key):
            setattr(recipe, key, value)

    await session.commit()
    await session.refresh(recipe)

    return recipe
