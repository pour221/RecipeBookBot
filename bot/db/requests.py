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


async def add_new_recipe(user_id, name, description):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        collection = await session.scalar(select(Collection).where(Collection.user_id == user.id))
        session.add(Recipe(user_id=user.id,
                           collection_id=collection.collection_id,
                           recipe_name=name,
                           descriptions=description,
                           ))
        await session.commit()

async def quick_add_new_recipe(user_id, name, description):
    await add_new_recipe(user_id, name, description)