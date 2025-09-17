from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from bot.keyboards.main_keyboard import main_menu
from bot.keyboards.recipes_keyboard import add_recipes_keyboard, get_scroll_list_kb
import bot.db.requests as request

main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message):
    await request.add_user(message.from_user.id,
                           message.from_user.username,
                   f'{message.from_user.first_name} {message.from_user.last_name}',
                          message.from_user.is_premium)

    await request.init_first_collection(message.from_user.id)

    photo = FSInputFile('../img/recipesbook.png')
    await message.answer_photo(photo=photo,
                                   caption='Main menu of *your recipes book*',
                                   reply_markup=main_menu, parse_mode=None)


@main_router.callback_query(F.data == 'find')
async def find_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'random')
async def random_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')


@main_router.callback_query(F.data == 'list')
async def list_recipe(callback: CallbackQuery):
    await callback.answer()
    page = 1

    # recipes = await request.get_list_recipes(callback.from_user.id)

    recipes, has_next, total_pages = await request.get_list_page(callback.from_user.id, page)

    if not recipes:
        await callback.message.answer(text='You do not have any recipes')
        return

    offset = (page - 1) * 20

    recipes_list = '\n'.join([f'{offset + num+1}. {i.recipe_name}' for num, i in enumerate(recipes)])
    await callback.message.answer(
        f'20 recipes are displayed. Use the menu to view the rest\n\nPage {page}/{total_pages}\n\n{recipes_list}',
                                  reply_markup=get_scroll_list_kb(page, has_next))

@main_router.callback_query(F.data.startswith("list_page:"))
async def next_page(callback: CallbackQuery):
    await callback.answer()

    page = int(callback.data.split(':')[1])

    recipes, has_next, total_pages = await request.get_list_page(callback.from_user.id, page)

    if not recipes:
        await callback.message.edit_text("You do not have any recipes")
        return

    offset = (page - 1) * 20
    recipes_list = '\n'.join([f'{offset + num + 1}. {i.recipe_name}' for num, i in enumerate(recipes)])
    await callback.message.edit_text(
        f'20 recipes are displayed. Use the menu to view the rest\n\nPage {page}/{total_pages}\n\n{recipes_list}',
                                  reply_markup=get_scroll_list_kb(page, has_next))


# @main_router.callback_query(F.data == 'list')
# async def list_recipe(callback: CallbackQuery):
#     await callback.answer()
#     page = 1
#
#     recipes = await request.get_list_recipes(callback.from_user.id)
#
#     if not recipes:
#         await callback.message.answer(text='You do not have any recipes')
#         return
#
#     recipes_list = '\n'.join([f'{num+1}. {i.recipe_name}' for num, i in enumerate(recipes)])
#     await callback.message.answer(f'20 recipes are displayed. Use the menu to view the rest\n\n{recipes_list}',
#                                   reply_markup=scroll_list_kb)

@main_router.callback_query(F.data == 'new_recipe')
async def new_recipe(callback: CallbackQuery):
    await callback.answer()
    photo = FSInputFile('../img/empty_page.png')
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