from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from bot.keyboards.main_keyboard import main_menu
start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    # async with open('../img/recipesbook_2.png', 'rb') as photo:
    photo = FSInputFile('../img/recipesbook_2.png')
    await message.answer_photo(photo=photo,
                                   caption='Main menu of *your recipes book*',
                                   reply_markup=main_menu, parse_mode=ParseMode.MARKDOWN_V2)
    # await message.answer('Main menu', reply_markup=main_menu)

@start_router.callback_query(F.data == 'find')
async def find_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@start_router.callback_query(F.data == 'random')
async def random_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@start_router.callback_query(F.data == 'list')
async def list_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@start_router.callback_query(F.data == 'new_recipe')
async def new_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@start_router.callback_query(F.data == 'change')
async def change_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@start_router.callback_query(F.data == 'new_collection')
async def new_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@start_router.callback_query(F.data == 'FeedBack')
async def feedback_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')