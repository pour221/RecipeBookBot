import asyncio
from aiogram import Bot, Dispatcher
from data.configs import TOKEN

from handlers.start import start_router
from handlers.recipie_handlers import recipe_router

from bot.db.session import async_main


async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(recipe_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())