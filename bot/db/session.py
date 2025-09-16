from data.configs import DB_PATH
from bot.db.models import Base, User, Collection, Ingredient, Recipe, RecipeIngredient
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import asyncio

engine = create_async_engine(url=f'sqlite+aiosqlite:///{DB_PATH}', echo=True)
async_session = async_sessionmaker(engine)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# asyncio.run(async_main())