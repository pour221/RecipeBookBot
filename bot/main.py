import asyncio
from aiogram import Bot, Dispatcher

from data.configs import TOKEN
from bot.handlers.main_handlers import main_router
from bot.handlers.recipie_handlers import recipe_router
from bot.db.session import async_main, async_session
from bot.middlewares.session_middleware import DbSessionMiddleware




async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(async_session))

    dp.include_router(main_router)
    dp.include_router(recipe_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())