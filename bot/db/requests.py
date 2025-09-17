from sqlalchemy import func
from bot.db.session import async_session
from bot.db.models.users import User
from bot.db.models import User, Collection, Recipe, RecipeIngredient, Ingredient
from datetime import datetime
from sqlalchemy.types import BigInteger

from sqlalchemy import select, update, delete

async def add_user(tg_id: BigInteger, user_name: str, fullname: str, tg_premium: bool):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id,
                             username=user_name,
                             fullname=fullname,
                             tg_premium=tg_premium,
                             created_at=datetime.utcnow(),
                             ))
            await session.commit()

async def init_first_collection(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))

        if not collection:
            session.add(Collection(user_id=user.id,
                                   name='Base'))
            await session.commit()

async def create_new_collection(user_id, collection_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        session.add(Collection(user_id=user.id,
                               name=collection_name))


async def add_new_recipe(user_id, name, description, ingredients_table, equipments, photos):
    async with async_session() as session:
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

async def quick_add_new_recipe(user_id, name, description):
    await add_new_recipe(user_id, name, description, None, None, None)

async def get_list_recipes(user_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))
        recipies = await session.scalars(select(Recipe).where(Recipe.collection_id == collection.collection_id))
        return recipies.all()

async def get_list_page(user_id, page, page_size=20):
    async with async_session() as session:
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

async def get_recipe_by_number(user_id: int, number: int) -> Recipe | None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))

        stmt = (
            select(Recipe)
            .where(Recipe.collection_id == collection.collection_id)
            .offset(number - 1)   # например, 7 → offset=6
            .limit(1)
        )
        result = await session.scalars(stmt)
        return result.first()
