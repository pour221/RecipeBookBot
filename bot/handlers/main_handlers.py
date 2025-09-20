from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.main_menu import show_main_menu
from bot.db.requests import add_user, init_first_collection
from bot.keyboards.recipes_keyboard import add_recipes_keyboard

from data.configs import pics

main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    await add_user(session, message.from_user.id,
                           message.from_user.username,
                   f'{message.from_user.first_name} {message.from_user.last_name}',
                          message.from_user.is_premium)

    await init_first_collection(session, message.from_user.id)
    await show_main_menu(message)

@main_router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    await show_main_menu(callback)

@main_router.callback_query(F.data == 'new_recipe')
async def new_recipe(callback: CallbackQuery):
    await callback.answer()
    photo = FSInputFile(pics['new'])
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption='Choose adding option'),
        reply_markup=add_recipes_keyboard
    )
@main_router.message(Command('cancel'))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Action canceled')
    await show_main_menu(message)

@main_router.callback_query(F.data == 'find')
async def find_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'random')
async def random_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'change')
async def change_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'new_collection')
async def new_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'FeedBack')
async def feedback_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')