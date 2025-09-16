from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from bot.keyboards.main_keyboard import main_menu
from bot.keyboards.add_recipes_keyboard import add_recipes_keyboard
import bot.db.requests as request

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await request.add_user(message.from_user.id,
                           message.from_user.username,
                   f'{message.from_user.first_name} {message.from_user.last_name}',
                          message.from_user.is_premium)

    await request.init_first_collection(message.from_user.id)

    photo = FSInputFile('../img/recipesbook.png')
    await message.answer_photo(photo=photo,
                                   caption='Main menu of *your recipes book*',
                                   reply_markup=main_menu, parse_mode=ParseMode.MARKDOWN_V2)


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
    await callback.answer()
    photo = FSInputFile('../img/empty_page.png')
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption='Choose adding option'),
        reply_markup=add_recipes_keyboard
    )



@start_router.callback_query(F.data == 'change')
async def change_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@start_router.callback_query(F.data == 'new_collection')
async def new_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@start_router.callback_query(F.data == 'FeedBack')
async def feedback_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')