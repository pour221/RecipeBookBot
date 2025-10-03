from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests.collection_requests import (create_new_collection, set_active_collection,
                                                 get_collection_by_id, delete_collection, rename_collection)

from bot.handlers.states import CollectionManage
from bot.db.models import User, Collection
from bot.services.pagination import get_pagination_kb, render_collection_list, get_obj_list
from bot.keyboards.collections_keyboard import (get_successfully_created_collection_kb,
                                                manage_collection_options_kb, get_successfully_change_active_collection_kb,
                                                get_successfully_delete_collection_kb)
from bot.services.formatting import safe_md
from bot.keyboards.callbacks import CollectionsCb, PaginationCb
from bot.keyboards.shared_keyboard import get_yes_no_kb

from data.configs import pics

collection_router = Router()

@collection_router.callback_query(PaginationCb.filter(F.action == 'collection_page'))
async def show_collection_list_page(callback: CallbackQuery, callback_data : PaginationCb, current_user: User,
                                    state: FSMContext, translation, session: AsyncSession):

    await state.set_state(CollectionManage.managing)

    page_size = 4
    page = callback_data.page

    collection_list, collections, has_next_page, total_pages = await render_collection_list(session, page, page_size,
                                                                                            current_user.id, translation)


    caption_text = translation('collections_list_text.list_msg', page=page, total_pages=total_pages,
                               collection_list=collection_list)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['list']),
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2),

                                      reply_markup=get_pagination_kb('collection', [i[0] for i in collections],
                                                                          page, page_size, has_next_page, translation,
                                                                          num_btn_row=2, action='manage'))
    await callback.answer()

@collection_router.callback_query(F.data == 'quick_change_collection')
async def quick_change_collection(callback: CallbackQuery, current_user: User, state: FSMContext,
                                  translation, session: AsyncSession):
    await state.set_state(CollectionManage.managing)
    page = 1
    page_size = 4
    photo = FSInputFile(pics['main'])
    caption_text = translation('collection_options_text.change')
    collections, has_next_page, total_pages = await get_obj_list(session, Collection, current_user.id, page=page,
                                                                 page_size=page_size)
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text),
                                      reply_markup=get_pagination_kb('collection', collections,
                                                                          page,page_size, has_next_page, translation,
                                                                          num_btn_row=2, action='set_active'))
    await callback.answer()

@collection_router.callback_query(F.data == 'create_collection')
async def new_collection(callback: CallbackQuery, state: FSMContext, translation):

    await state.set_state(CollectionManage.waiting_new_collection_name)

    photo = FSInputFile(pics['main'])
    caption_text = translation("collection_create_text.invitation")
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text))
    await callback.answer()

@collection_router.message(CollectionManage.waiting_new_collection_name)
async def receiving_new_collection_name(message: Message, state: FSMContext,
                                      current_user: User, translation, session: AsyncSession):
    new_name = message.text
    await create_new_collection(session, current_user, new_name)
    await state.clear()
    await message.answer_photo(photo=FSInputFile(pics['adding']),
                               caption=translation('collection_create_text.success'),
                               reply_markup=get_successfully_created_collection_kb(translation))

@collection_router.callback_query(CollectionManage.managing, CollectionsCb.filter(F.action.startswith('manage')))
async def manage_collection(callback: CallbackQuery, callback_data: CollectionsCb,
                            translation, session: AsyncSession):

    collection = await get_collection_by_id(session, callback_data.obj_id)

    photo = FSInputFile(pics['adding'])
    caption_text = translation('collection_options_text.text', collection_name=safe_md(collection.name))

    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=manage_collection_options_kb(callback_data.obj_id, collection.name,
                                                                                callback_data.page, translation))

@collection_router.callback_query(CollectionManage.managing, CollectionsCb.filter(F.action == 'set_active'))
async def change_active_collection(callback: CallbackQuery, callback_data: CollectionsCb,
                                   current_user: User, translation, session: AsyncSession):

    requested_collection_id = callback_data.obj_id
    if  current_user.active_collection_id == requested_collection_id:
        await callback.answer(translation('collection_options_text.change_current_active'), show_alert=True)
        return
    await set_active_collection(session, current_user.id, requested_collection_id)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                            caption=translation('collection_options_text.success_change'),
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_successfully_change_active_collection_kb(callback_data.page,
                                                                                                callback_data.obj_id,
                                                                                                translation))
    await callback.answer()

@collection_router.callback_query(CollectionManage.managing, CollectionsCb.filter(F.action == 'delete_collection'))
async def delete_collection_request(callback: CallbackQuery, callback_data: CollectionsCb,
                                    translation, session: AsyncSession):
    collection = await get_collection_by_id(session, callback_data.obj_id)
    caption_text = translation('collection_options_text.confirm_deletion', collection_name=collection.name)
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_yes_no_kb(cb_class=CollectionsCb, yes_action='confirmed_collection_deletion',
                                                                 no_action='manage', obj_id=callback_data.obj_id, translation=translation))



@collection_router.callback_query(CollectionManage.managing, CollectionsCb.filter(F.action == 'confirmed_collection_deletion'))
async def delete_collection_confirm(callback: CallbackQuery, callback_data: CollectionsCb,
                                    session: AsyncSession, current_user: User, translation,
                                    base_collection_id):

    is_deleted = False

    requested_collection_id = callback_data.obj_id
    if requested_collection_id == base_collection_id:
        await callback.answer(translation('collection_options_text.try_to_delete_base'))
        return

    if requested_collection_id == current_user.active_collection_id:
        await set_active_collection(session, current_user.id, base_collection_id)
        await session.refresh(current_user)


    is_deleted = await delete_collection(session, current_user.id, requested_collection_id, base_collection_id)

    if is_deleted:
        photo = FSInputFile(pics['adding'])
        caption_text = translation('collection_options_text.success_delete')
    else:
        photo = FSInputFile(pics['adding'])
        caption_text = translation('collection_options_text.unsuccess_delete')

    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_successfully_delete_collection_kb(translation))
    await callback.answer()

@collection_router.callback_query(CollectionManage.managing, CollectionsCb.filter(F.action == 'rename_collection'))
async def get_new_collection_name(callback: CallbackQuery, callback_data: CollectionsCb,
                                  translation, state: FSMContext):
    photo = FSInputFile(pics['adding'])
    caption_text = translation('collection_options_text.rename')
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text))
    await state.update_data(collection_id_to_rename=callback_data.obj_id,
                            collection_page=callback_data.page)
    await state.set_state(CollectionManage.waiting_for_value)
    await callback.answer()

@collection_router.message(CollectionManage.waiting_for_value)
async def change_collection_name(message: Message, current_user: User, state: FSMContext,
                                 translation, session: AsyncSession):
    data = await state.get_data()
    collection_id = data.get('collection_id_to_rename')
    page = data.get('collection_page')

    is_change = await rename_collection(session, collection_id, current_user.id, message.text)

    if is_change:
        photo = FSInputFile(pics['adding'])
        caption_text = translation('collection_options_text.success_rename')
    else:
        photo = FSInputFile(pics['adding'])
        caption_text = translation('collection_options_text.unsuccess_rename')

    await message.answer_photo(photo=photo,
                               caption=caption_text,
                               reply_markup=get_successfully_change_active_collection_kb(page, collection_id, translation))

    await state.clear()
    await state.set_state(CollectionManage.managing)
