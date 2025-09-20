import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.enums import ParseMode

from bot.db.requests import (quick_add_new_recipe, delete_recipe_by_id, get_list_page, get_recipe_by_id,
                             update_recipe)
from bot.handlers.states import QuickRecipe, EditRecipe
from bot.keyboards.recipes_keyboard import (get_recipe_option_kb, get_recipe_list_kb,
                                            get_confirm_delete_kb, get_edit_options_kb,
                                            EDITABLE_RECIPE_FIELDS, successfully_update_recipe_field_options) # add_recipes_keyboard
from bot.services.main_menu import show_main_menu
from bot.utils.formatting import safe_md

from data.configs import pics

recipe_router = Router()

@recipe_router.callback_query(F.data == 'quick_add')
async def quick_add(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(QuickRecipe.name)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                            caption='Write recipe *title*:',
                                                            parse_mode=ParseMode.MARKDOWN_V2))
    # await state.update_data(last_msg_id=msg.id)

@recipe_router.message(QuickRecipe.name)
async def recipe_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await state.set_state(QuickRecipe.description)
    await message.answer_photo(photo=FSInputFile(pics['adding']), caption='Write your *recipe description*:',
                             parse_mode=ParseMode.MARKDOWN_V2)


@recipe_router.message(QuickRecipe.description)
async def recipe_description(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.text)
    data = await state.get_data()

    await quick_add_new_recipe(session, message.from_user.id, data["name"], data["description"], )
    await message.answer(safe_md(f'Your recipe *"{data["name"]}"* has been added !'), parse_mode=ParseMode.MARKDOWN_V2)
    await state.clear()
    await show_main_menu(message)

@recipe_router.callback_query(F.data == 'detailed_add')
async def quick_add(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@recipe_router.callback_query(F.data == 'ai_generate')
async def quick_add(callback: CallbackQuery):
    await callback.answer('AI not ready right now, sorry. You can try another adding options')

@recipe_router.callback_query(F.data == 'new_option')
async def quick_add(callback: CallbackQuery):
    await callback.answer('New amazing options will be here very soon. Stay tuned!')

# @recipe_router.callback_query(F.data == 'pick')
# async def pick_recipe_by_number(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#     await state.set_state(RecipeListState.waiting_for_number)
#     await callback.message.answer('Write recipe number')

# @recipe_router.message(RecipeListState.waiting_for_number, F.text.regexp(r"^\d+$"))
# async def get_recipe_number(message: Message, state: FSMContext, session: AsyncSession):
#     recipe_number = int(message.text)
#     recipe = await get_recipe_by_number(session, message.from_user.id, recipe_number)
#     if not recipe:
#         await message.answer(f"No recipe with number {recipe_number}")
#         return
#
#     recipe_msg = safe_md(f'{recipe.recipe_name.title()}\n\n{recipe.descriptions}')
#     photo = FSInputFile(pics['my'])
#     await message.answer_photo(photo=photo, caption=recipe_msg, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=get_recipe_option_kb(rec))
#     await state.clear()

@recipe_router.callback_query(F.data == 'list')
async def list_recipe(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    page = 1
    offset = (page - 1) * 12

    recipes, has_next, total_pages = await get_list_page(session, callback.from_user.id, page)

    if not recipes:
        await callback.message.answer(text='You do not have any recipes')
        return


    recipes_list = '\n'.join([f'{offset + num+1}. {i.recipe_name}' for num, i in enumerate(recipes)])
    caption_text = safe_md(f'{len(recipes)} recipes are displayed. Use the menu to view the rest\n\nPage {page}/{total_pages}\n\n{recipes_list}')
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile(pics['list']),
                              caption= caption_text,
                              parse_mode=ParseMode.MARKDOWN_V2),
        reply_markup=get_recipe_list_kb(recipes, offset, page, has_next))

@recipe_router.callback_query(F.data.startswith("list_page:"))
async def next_page(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()

    page = int(callback.data.split(':')[1])
    offset = (page - 1) * 12

    recipes, has_next, total_pages = await get_list_page(session, callback.from_user.id, page)

    if not recipes:
        await callback.message.edit_text("You do not have any recipes")
        return


    recipes_list = '\n'.join([f'{offset + num + 1}. {i.recipe_name}' for num, i in enumerate(recipes)])
    caption_text = safe_md(f'{len(recipes)} recipes are displayed. Use the menu to view the rest\n\nPage {page}/{total_pages}\n\n{recipes_list}')
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['list']),
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                  reply_markup=get_recipe_list_kb(recipes, offset, page, has_next))


@recipe_router.callback_query(F.data.startswith("recipe:"))
async def show_recipe(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    recipe_id = int(callback.data.split(":")[1])
    recipe = await get_recipe_by_id(session, recipe_id)

    if not recipe:
        await callback.messsage.answer("Recipe not found")
        return

    recipe_msg = f'*{safe_md(recipe.recipe_name.title())}*\n\n{safe_md(recipe.descriptions)}'
    photo = FSInputFile(pics['my'])
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=recipe_msg,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_recipe_option_kb(recipe_id))


@recipe_router.callback_query(F.data.startswith('edit_recipe:'))
async def edit_recipe(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    recipe_id = int(callback.data.split(":")[1])
    recipe = await get_recipe_by_id(session, recipe_id)

    caption_text = f'*{safe_md(recipe.recipe_name.title())}*\n\n{safe_md(recipe.descriptions)}\n\nChoose what to change in the recipe'

    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_edit_options_kb(recipe_id, ))

@recipe_router.callback_query(F.data.startswith('edit_field:'))
async def edit_recipe_field(callback: CallbackQuery, state: FSMContext):
    _, field, recipe_id = callback.data.split(":")
    caption_text = f'Write new {safe_md(EDITABLE_RECIPE_FIELDS[field])}'
    await state.update_data(recipe_id=int(recipe_id), field=field)
    await callback.message.edit_media(
        InputMediaPhoto(media=FSInputFile(pics['adding']),
                        caption=caption_text,
                        parse_mode=ParseMode.MARKDOWN_V2)
    )
    await state.set_state(EditRecipe.waiting_for_value)

@recipe_router.message(EditRecipe.waiting_for_value)
async def update_recipe_field(message: Message, session: AsyncSession, state:FSMContext):
    data = await state.get_data()
    recipe_id = data['recipe_id']
    field = data['field']

    kwargs = {field: message.text}
    updated = await update_recipe(session, recipe_id, **kwargs)

    if updated:
        await message.answer(f'{EDITABLE_RECIPE_FIELDS[field]} successfully updated',
                             reply_markup=successfully_update_recipe_field_options(recipe_id))
    else:
        await message.answer(f'Update failed: This recipe cannot be updated.')

    await state.clear()

# async def quick_recipe_edit(callback: CallbackQuery, session: AsyncSession):
#     recipe_id = int(callback.data.split(':')[1])
#
#
# @recipe_router.callback_query(F.data.startswith('detail_edit:'))
# async def quick_recipe_edit(callback: CallbackQuery, session: AsyncSession):
#     await callback.answer('Not available yet')

@recipe_router.callback_query(F.data.startswith('delete_recipe:'))
async def delete_recipe(callback: CallbackQuery, session: AsyncSession):
    recipe_id = int(callback.data.split(":")[1])
    recipe = await get_recipe_by_id(session, recipe_id)

    caption_text = f'Are you sure you want to delete the *{safe_md(recipe.recipe_name)}* recipe?'
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_confirm_delete_kb(recipe_id))

@recipe_router.callback_query(F.data.startswith('confirm_delete_recipe:'))
async def confirm_delete_recipe(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    recipe_id = int(callback.data.split(":")[1])
    recipe = await get_recipe_by_id(session, recipe_id)

    caption_text = f'The recipe *{safe_md(recipe.recipe_name)}* has been deleted'

    await delete_recipe_by_id(session, recipe)
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2))
    await asyncio.sleep(0.5)
    await show_main_menu(callback)

