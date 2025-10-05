from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.enums import ParseMode

from bot.db.requests import (quick_add_new_recipe, delete_recipe_by_id, get_recipe_by_id,
                             update_recipe)
from bot.handlers.states import QuickRecipe, RecipeManage
from bot.keyboards.recipes_keyboard import (get_recipe_option_kb, get_edit_options_kb,
                                            get_successfully_update_recipe_field_kb,
                                            get_successfully_delete_recipe_kb, get_successfully_added_recipe_kb,
                                            get_add_recipes_keyboard)
from bot.keyboards.shared_keyboard import get_yes_no_kb
from bot.keyboards.callbacks import RecipeCb, PaginationCb
from bot.services.main_menu import show_main_menu
from bot.services.formatting import safe_md, get_recipe_photo, render_recipe_text
from bot.db.models import User
from bot.services.pagination import render_recipe_list, get_pagination_kb

from data.configs import pics


recipe_router = Router()

@recipe_router.callback_query(F.data.startswith('quick_add:'))
async def quick_add(callback: CallbackQuery, translation, state: FSMContext):
    await state.set_state(QuickRecipe.name)
    target_collection = callback.data.split(':')[1]
    await state.update_data(target_collection=target_collection)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['new_recipe']),
                                                            caption=translation('quick_add_text.title'),
                                                            parse_mode=ParseMode.MARKDOWN_V2))
    await callback.answer()

@recipe_router.message(QuickRecipe.name)
async def receive_recipe_name(message: Message, translation, state: FSMContext): # old name: recipe_name
    await state.update_data(name=message.text.title())
    await state.set_state(QuickRecipe.description)
    await message.answer_photo(photo=FSInputFile(pics['new_recipe']), caption=translation('quick_add_text.description'),
                             parse_mode=ParseMode.MARKDOWN_V2)

@recipe_router.message(QuickRecipe.description)
async def recipe_description(message: Message, state: FSMContext, current_user: User,
                            translation, session: AsyncSession):

    await state.update_data(description=message.text)
    data = await state.get_data()

    target_collection = data.get('target_collection')

    await quick_add_new_recipe(session, current_user, target_collection, data["name"], data["description"], )
    await message.answer(text=translation('quick_add_text.success', name=safe_md(data["name"])), parse_mode=ParseMode.MARKDOWN_V2,
                         reply_markup=get_successfully_added_recipe_kb(translation, target_collection))
    await state.clear()

@recipe_router.callback_query(F.data.startswith('detailed_add:'))
async def quick_add(callback: CallbackQuery):
    await callback.answer('Will be available soon')

@recipe_router.callback_query(F.data == 'ai_generate')
async def quick_add(callback: CallbackQuery):
    await callback.answer('AI not ready right now, sorry. You can try another adding options')

@recipe_router.callback_query(F.data == 'new_option')
async def quick_add(callback: CallbackQuery):
    await callback.answer('New amazing options will be here very soon. Stay tuned!')

@recipe_router.callback_query(PaginationCb.filter(F.action == 'recipe_page'))
async def show_recipe_list_page(callback: CallbackQuery, callback_data: PaginationCb,
                                translation, current_user: User, session: AsyncSession,
                                state: FSMContext):
    await state.clear()

    page_size = 12
    collection_id = callback_data.obj_id
    page = callback_data.page

    if not collection_id:
        collection_id = current_user.active_collection_id
    else:
        collection_id = int(collection_id)

    if not page:
        page = 1
    else:
        page = int(page)

    recipes_list, recipes, has_next, total_pages = await render_recipe_list(session, page, page_size, collection_id,
                                                                            current_user.id)

    if not recipes:
        await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['empty_list']),
                                                          caption=translation('adding_text.no_recipe')),
                                          reply_markup=get_add_recipes_keyboard(translation, collection_id))

        await callback.answer()
        return

    caption_text = translation('recipe_list_text.displayed', recipe_number=len(recipes), page=page,
                               total_pages=total_pages, recipes_list=safe_md(recipes_list))

    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['recipe_list']),
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_pagination_kb('recipe', recipes, page,
                                                                          page_size, has_next, translation,
                                                                          num_btn_row=4, collection_id=collection_id,
                                                                          action='show_recipe'))
    await callback.answer()



@recipe_router.callback_query(RecipeCb.filter(F.action == "show_recipe"))
async def show_recipe(callback: CallbackQuery, callback_data: RecipeCb, active_collection_name: str,
                      translation, state: FSMContext, session: AsyncSession):
    await state.set_state(RecipeManage.managing)
    recipe = await get_recipe_by_id(session, callback_data.obj_id)

    await state.update_data(recipe=recipe)

    if not recipe:
        await callback.message.answer(translation('recipe_list_text.not_found'))
        await show_main_menu(callback, active_collection_name, True)

        return

    recipe_msg = render_recipe_text(recipe, translation)
    photo = FSInputFile(get_recipe_photo(recipe))
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=recipe_msg,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_recipe_option_kb(callback_data.obj_id, callback_data.page,
                                                                        translation))

    await callback.answer()

@recipe_router.callback_query(RecipeManage.managing, RecipeCb.filter(F.action == "edit_recipe"))
async def  edit_recipe(callback: CallbackQuery, callback_data: RecipeCb, translation, state: FSMContext):

    context_data = await state.get_data()
    recipe = context_data['recipe']
    caption_text = translation('editing_text.choose_what', recipe_name=safe_md(recipe.recipe_name.title()),
                                                           descriptions=safe_md(recipe.descriptions))

    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['edit']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_edit_options_kb(callback_data.obj_id, callback_data.page,
                                                                       translation))
    await callback.answer()

@recipe_router.callback_query(RecipeManage.managing, RecipeCb.filter(F.action == "delete_recipe"))
async def delete_recipe(callback: CallbackQuery, callback_data: RecipeCb, translation, state: FSMContext):
    context_data = await state.get_data()
    recipe = context_data['recipe']
    page= callback_data.page

    caption_text = translation('delete_text.delete_question', recipe_name=recipe.recipe_name)
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['delete']),

                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_yes_no_kb(cb_class=RecipeCb, yes_action='confirm_delete_recipe', no_action='show_recipe',
                                                                 page=page,obj_id=recipe.recipe_id, translation=translation))

    await callback.answer()

@recipe_router.callback_query(RecipeManage.managing, RecipeCb.filter(F.action == "confirm_delete_recipe"))
async def confirm_delete_recipe(callback: CallbackQuery, callback_data: RecipeCb, state: FSMContext,
                                translation, session: AsyncSession):

    context_data = await state.get_data()
    recipe = context_data['recipe']
    caption_text = translation('delete_text.delete_confirmation', recipe_name=recipe.recipe_name)
    await delete_recipe_by_id(session, recipe)

    await state.clear()
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['delete']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_successfully_delete_recipe_kb(callback_data.page, translation))
    await callback.answer()

@recipe_router.callback_query(RecipeManage.managing, F.data.startswith('edit_field:'))
async def edit_recipe_field(callback: CallbackQuery, state: FSMContext, translation):
    _, field, recipe_id = callback.data.split(":")

    context_data = await state.get_data()
    recipe = context_data['recipe']

    caption_text = translation('editing_text.write', recipe_name=safe_md(recipe.recipe_name.title()),
                                                     description=safe_md(recipe.descriptions),
                                                     field=translation(f'editable_fields.{field}').lower())
    await state.update_data(field=field)
    await callback.message.edit_media(
        InputMediaPhoto(media=FSInputFile(pics['edit']),
                        caption=caption_text,
                        parse_mode=ParseMode.MARKDOWN_V2)
    )
    await state.set_state(RecipeManage.waiting_for_value)

@recipe_router.message(RecipeManage.waiting_for_value)
async def update_recipe_field(message: Message, state:FSMContext, translation, session: AsyncSession):
    data = await state.get_data()
    recipe = data['recipe']
    field = data['field']

    kwargs = {field: message.text}
    updated = await update_recipe(session, recipe.recipe_id, **kwargs)
    await state.update_data(recipe=await get_recipe_by_id(session, recipe.recipe_id))
    if updated:
        msg_text = translation('editing_text.success', field=translation(f'editable_fields.{field}').title(),
                                                       recipe_name=safe_md(updated.recipe_name.title()),
                                                       description=safe_md(updated.descriptions))
        await message.answer(text=msg_text,
                             reply_markup=get_successfully_update_recipe_field_kb(recipe.recipe_id, translation),
                             parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await message.answer(translation('editing_text.unsuccess'))

    await state.set_state(RecipeManage.managing)

