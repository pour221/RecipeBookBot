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

async def get_list_page(session: AsyncSession, user_id, page, page_size=12):
    user = await session.scalar(select(User).where(User.tg_id == user_id))
    collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))

    total = await session.scalars(select(Recipe).where(Recipe.collection_id == collection.collection_id))

    stmt = (
            select(Recipe)
            .where(Recipe.collection_id == collection.collection_id)
            .limit(page_size+1)
            .offset((page-1)*page_size)
        )

    results = await session.scalars(stmt)
    recipes = results.all()

    total_pages = (len(total.all()) + page_size - 1) // page_size
    #max(1, (len(total.all()) + page_size - 1) // page_size)

    has_next = len(recipes) > page_size
    return recipes[:page_size], has_next, total_pages

# async def get_recipe_by_number(session: AsyncSession, user_id: int, number: int) -> Recipe | None:
#     user = await session.scalar(select(User).where(User.tg_id == user_id))
#     collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))
#
#     stmt = (
#             select(Recipe)
#             .where(Recipe.collection_id == collection.collection_id)
#             .offset(number - 1)
#             .limit(1)
#         )
#     result = await session.scalars(stmt)
#     return result.first()

async def get_recipe_by_id(session: AsyncSession, recipe_id):
    return await session.get(Recipe, recipe_id)

async def delete_recipe_by_id(session: AsyncSession, recipe):
    await session.delete(recipe)
    await session.commit()

# async def update_recipe(session: AsyncSession, recipe_id: int, name: str | None,
#                         description: str | None, ingredients_table: str | None,
#                         equipments: str | None, photos: str | None):
#     recipe = await session.scalar(select(Recipe).where(Recipe.recipe_id == recipe_id))
#
#     if name is not None:
#         recipe.recipe_name = name
#
#     if description is not None:
#         recipe.descriptions = description
#
#     if ingredients_table is not None:
#         recipe.ingredients_table = ingredients_table
#
#     if equipments is not None:
#         recipe.equipments = equipments
#
#     if photos is not None:
#         recipe.photos = photos
#
#     await session.commit()
#     await session.refresh(recipe)
#
#     return recipe
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
