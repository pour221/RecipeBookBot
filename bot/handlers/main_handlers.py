from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.main_menu import show_main_menu
from bot.keyboards.recipes_keyboard import add_recipes_keyboard, get_scroll_list_kb
from bot.db.requests import add_user, init_first_collection, get_list_page

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

@main_router.callback_query(F.data == 'find')
async def find_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'random')
async def random_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')


@main_router.callback_query(F.data == 'list')
async def list_recipe(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    page = 1

    recipes, has_next, total_pages = await get_list_page(session, callback.from_user.id, page)

    if not recipes:
        await callback.message.answer(text='You do not have any recipes')
        return

    offset = (page - 1) * 20

    recipes_list = '\n'.join([f'{offset + num+1}. {i.recipe_name}' for num, i in enumerate(recipes)])
    await callback.message.answer(
        f'20 recipes are displayed. Use the menu to view the rest\n\nPage {page}/{total_pages}\n\n{recipes_list}',
                                  reply_markup=get_scroll_list_kb(page, has_next))

@main_router.callback_query(F.data.startswith("list_page:"))
async def next_page(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    page = int(callback.data.split(':')[1])

    recipes, has_next, total_pages = await get_list_page(session, callback.from_user.id, page)

    if not recipes:
        await callback.message.edit_text("You do not have any recipes")
        return

    offset = (page - 1) * 20
    recipes_list = '\n'.join([f'{offset + num + 1}. {i.recipe_name}' for num, i in enumerate(recipes)])
    await callback.message.edit_text(
        f'20 recipes are displayed. Use the menu to view the rest\n\nPage {page}/{total_pages}\n\n{recipes_list}',
                                  reply_markup=get_scroll_list_kb(page, has_next))

@main_router.callback_query(F.data == 'new_recipe')
async def new_recipe(callback: CallbackQuery):
    await callback.answer()
    photo = FSInputFile(pics['new'])
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption='Choose adding option'),
        reply_markup=add_recipes_keyboard
    )


@main_router.callback_query(F.data == 'change')
async def change_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'new_collection')
async def new_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'FeedBack')
async def feedback_collection(callback: CallbackQuery):
    await callback.answer('Not ready yet')