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
                                            AVAILABLE_RECIPE_FIELDS, successfully_update_recipe_field_options,
                                            successfully_delete_recipe_options, successfully_added_recipe_kb, get_no_recipe_kb) # add_recipes_keyboard
from bot.keyboards.callbacks import RecipeCb, RecipeListCb
from bot.services.main_menu import show_main_menu
from bot.utils.formatting import safe_md
from bot.db.models import User, Collection
from bot.services.recipe_list import render_recipe_list

from data.configs import pics


recipe_router = Router()

@recipe_router.callback_query(F.data == 'quick_add')
async def quick_add(callback: CallbackQuery, translation, state: FSMContext):
    await state.set_state(QuickRecipe.name)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                            caption=translation('quick_add_text.title'),
                                                            parse_mode=ParseMode.MARKDOWN_V2))
    await callback.answer()

@recipe_router.message(QuickRecipe.name)
async def recipe_name(message: Message, translation, state: FSMContext):
    await state.update_data(name=message.text.title())
    await state.set_state(QuickRecipe.description)
    await message.answer_photo(photo=FSInputFile(pics['adding']), caption=translation('quick_add_text.description'),
                             parse_mode=ParseMode.MARKDOWN_V2)

@recipe_router.message(QuickRecipe.description)
async def recipe_description(message: Message, state: FSMContext, current_user: User,
                             active_collection: Collection, translation,
                             session: AsyncSession):

    await state.update_data(description=message.text)
    data = await state.get_data()
    await quick_add_new_recipe(session, current_user, active_collection, data["name"], data["description"], )
    await message.answer(text=translation('quick_add_text.success', name=safe_md(data["name"])), parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=successfully_added_recipe_kb)
    await state.clear()

@recipe_router.callback_query(F.data == 'detailed_add')
async def quick_add(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@recipe_router.callback_query(F.data == 'ai_generate')
async def quick_add(callback: CallbackQuery):
    await callback.answer('AI not ready right now, sorry. You can try another adding options')

@recipe_router.callback_query(F.data == 'new_option')
async def quick_add(callback: CallbackQuery):
    await callback.answer('New amazing options will be here very soon. Stay tuned!')

@recipe_router.callback_query(RecipeListCb.filter(F.action == 'list_page'))
async def show_recipe_list_page(callback: CallbackQuery, callback_data: RecipeListCb,
                                translation, active_collection: Collection, session: AsyncSession):
    page_size = 12
    collection_id = callback_data.collection_id
    page = callback_data.page

    if not collection_id:
        collection_id = active_collection.collection_id
    else:
        collection_id = int(collection_id)

    if not page:
        page = 1
    else:
        page = int(page)

    offset = (page - 1) * page_size
    recipes_list, recipes, has_next, total_pages = await render_recipe_list(session, page, page_size, collection_id)

    if not recipes:
        await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['list']),
                                                          caption=translation('adding_text.no_recipe')),
                                          reply_markup=get_no_recipe_kb(translation))

        await callback.answer()
        return

    # caption_text = safe_md(f'{len(recipes)} recipes are displayed. Use the menu to view the rest\n\nPage {page}/{total_pages}\n\n{recipes_list}')
    caption_text = translation('recipe_list_text.displayed', recipe_number=len(recipes), page=page, total_pages=total_pages,
                               recipes_list=safe_md(recipes_list))

    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['list']),
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_recipe_list_kb(recipes, offset, page, has_next, collection_id))
    await callback.answer()



@recipe_router.callback_query(RecipeCb.filter(F.action == "show_recipe"))
async def show_recipe(callback: CallbackQuery, callback_data: RecipeCb, active_collection: Collection,
                      translation, session: AsyncSession):
    recipe = await get_recipe_by_id(session, callback_data.recipe_id)

    if not recipe:
        await callback.message.answer(translation('recipe_list_text.not_found'))
        await show_main_menu(callback, active_collection.name, True)

        return

    recipe_msg = f'*{safe_md(recipe.recipe_name.title())}*\n\n{safe_md(recipe.descriptions)}'
    photo = FSInputFile(pics['my'])
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=recipe_msg,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_recipe_option_kb(callback_data.recipe_id, callback_data.page))
    await callback.answer()

@recipe_router.callback_query(RecipeCb.filter(F.action == "edit_recipe"))
async def  edit_recipe(callback: CallbackQuery, callback_data: RecipeCb, session: AsyncSession):
    recipe = await get_recipe_by_id(session, callback_data.recipe_id)
    caption_text = f'*{safe_md(recipe.recipe_name.title())}*\n\n{safe_md(recipe.descriptions)}\n\nChoose what to change in the recipe'
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_edit_options_kb(callback_data.recipe_id, callback_data.page))
    await callback.answer()

@recipe_router.callback_query(RecipeCb.filter(F.action == "delete_recipe"))
async def delete_recipe(callback: CallbackQuery, callback_data: RecipeCb, session: AsyncSession):
    recipe = await get_recipe_by_id(session, callback_data.recipe_id)
    caption_text = f'Are you sure you want to delete the *{safe_md(recipe.recipe_name)}* recipe?'
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_confirm_delete_kb(callback_data.recipe_id, callback_data.page))
    await callback.answer()

@recipe_router.callback_query(RecipeCb.filter(F.action == "confirm_delete_recipe"))
async def confirm_delete_recipe(callback: CallbackQuery, callback_data: RecipeCb, session: AsyncSession):
    recipe = await get_recipe_by_id(session, callback_data.recipe_id)
    caption_text = f'The recipe *{safe_md(recipe.recipe_name)}* has been deleted'
    await delete_recipe_by_id(session, recipe)
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=successfully_delete_recipe_options(callback_data.page))
    await callback.answer()

@recipe_router.callback_query(F.data.startswith('edit_field:'))
async def edit_recipe_field(callback: CallbackQuery, session:AsyncSession, state: FSMContext):
    _, field, recipe_id = callback.data.split(":")
    recipe = await get_recipe_by_id(session, recipe_id)
    caption_text = f'*{safe_md(recipe.recipe_name.title())}*\n\n{safe_md(recipe.descriptions)}\n\nWrite new {safe_md(AVAILABLE_RECIPE_FIELDS[field])}'
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
        msg_text = f'{AVAILABLE_RECIPE_FIELDS[field]} successfully updated\nUpdated recipe:\n\n*{safe_md(updated.recipe_name.title())}*\n\n{safe_md(updated.descriptions)}\n\n'
        await message.answer(text=msg_text,
                             reply_markup=successfully_update_recipe_field_options(recipe_id),
                             parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await message.answer(f'Update failed: This recipe cannot be updated.')

    await state.clear()

