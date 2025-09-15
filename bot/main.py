import asyncio
from handlers.start import start_router
from aiogram import Bot, Dispatcher
from data.configs import TOKEN

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


# import os
#
# print(f'Here we start out bot. PWD is {os.getcwd()}')
