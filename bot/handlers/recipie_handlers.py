from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

import bot.db.requests as request
from bot.handlers.states import QuickRecipe
from bot.keyboards.main_keyboard import main_menu

recipe_router = Router()

@recipe_router.callback_query(F.data == 'quick_add')
async def quick_add(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(QuickRecipe.name)
    await callback.message.answer('Write recipe title')

@recipe_router.message(QuickRecipe.name)
async def recipe_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(QuickRecipe.description)
    await message.answer('Write your recipe')

@recipe_router.message(QuickRecipe.description)
async def recipe_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    # await message.answer(f'Title: {data["name"]}\nDescription: {data["description"]}\nphotos: {data["photos"]}')
    await request.quick_add_new_recipe(message.from_user.id, data["name"], data["description"], )
    await message.answer(f'Title: {data["name"]}\nDescription: {data["description"]}')
    await message.answer('Your recipe was add!')
    await state.clear()
    photo = FSInputFile('../img/recipesbook.png')
    await message.answer_photo(photo=photo, caption='Main menu of *your recipes book*', reply_markup=main_menu,
                               parse_mode=ParseMode.MARKDOWN_V2)
    # await state.set_state(QuickRecipe.photos)
    # await message.answer('Add photos if you want (NOT WORKING RIGHT NOW)')

# @recipe_router.message(QuickRecipe.photos)
# async def recipe_photos(message: Message, state: FSMContext):
#     if message.photo:
#         await state.update_data(photos=message.photo)
#     else:
#         await state.update_data(photos=None)
#     data = await state.get_data()
#     # await message.answer(f'Title: {data["name"]}\nDescription: {data["description"]}\nphotos: {data["photos"]}')
#     await request.quick_add_new_recipe(message.from_user.id, data["name"],data["description"],)
#     await message.answer(f'Title: {data["name"]}\nDescription: {data["description"]}\nphotos: {data["photos"]}')
#     await message.answer('Your recipe was add!')
#     await state.clear()
#     photo = FSInputFile('../img/recipesbook.png')
#     await message.answer_photo(photo=photo, caption='Main menu of *your recipes book*', reply_markup=main_menu,
#                                parse_mode=ParseMode.MARKDOWN_V2)


@recipe_router.callback_query(F.data == 'detailed_add')
async def quick_add(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@recipe_router.callback_query(F.data == 'ai_generate')
async def quick_add(callback: CallbackQuery):
    await callback.answer('AI not ready right now, sorry. You can try another adding options')

@recipe_router.callback_query(F.data == 'new_option')
async def quick_add(callback: CallbackQuery):
    await callback.answer('New amazing options will be here very soon. Stay tuned!')

@recipe_router.callback_query(F.data == 'main_menu')
async def quick_add(callback: CallbackQuery):
    photo = FSInputFile('../img/recipesbook.png')
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption='Main menu of *your recipes book*', parse_mode=ParseMode.MARKDOWN_V2),
        reply_markup=main_menu,
    )
    await callback.answer()