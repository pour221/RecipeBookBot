# from models import Base, User, Collection, Ingredient, Recipe, RecipeIngredient
#
from models import Base, User, Collection, Ingredient, Recipe, RecipeIngredient
# from base import Base
# from models.users import User
# from models.collections import Collection
# from models.ingredient import Ingredient
# from models.recipes import Recipe
# from models.recipes import RecipeIngredient
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import asyncio

engine = create_async_engine(url='sqlite+aiosqlite:///../../data/db/db.sqlite3', echo=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(async_main())