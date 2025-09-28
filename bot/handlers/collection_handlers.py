from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests.collection_requests import (create_new_collection, get_collection_list_page, set_active_collection,
                                                 get_collection_by_id, delete_collection, rename_collection)

from bot.handlers.states import NewCollection, RenameCollection
from bot.db.models import User, Collection
from bot.keyboards.collections_keyboard import (successfully_created_collection_kb, get_collection_list_kb,
                                                manage_collection_options_kb, successfully_change_active_collection_kb,
                                                get_collection_delete_confirmation_kb)
from bot.utils.formatting import safe_md
from bot.keyboards.callbacks import CollectionsCb

from data.configs import pics

collection_router = Router()

@collection_router.callback_query(F.data == 'create_collection')
async def new_collection(callback: CallbackQuery, state: FSMContext, translation):

    await state.set_state(NewCollection.waiting_new_collection_name)

    photo = FSInputFile(pics['main'])
    caption_text = translation("collection_create_text.invitation")#'Write name for your new collection.\n\n/cancel - cancel this action'
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text))
    await callback.answer()

@collection_router.message(NewCollection.waiting_new_collection_name)
async def receiving_new_collection_name(message: Message, state: FSMContext,
                                      current_user: User, translation, session: AsyncSession):
    new_name = message.text
    await create_new_collection(session, current_user, new_name)
    await state.clear()
    await message.answer_photo(photo=FSInputFile(pics['adding']),
                               caption=translation('collection_create_text.success'),
                               reply_markup=successfully_created_collection_kb)

@collection_router.callback_query(F.data == 'quick_change_collection')
async def quick_change_collection(callback: CallbackQuery, current_user: User,
                                  translation, session: AsyncSession):
    page = 1
    page_size = 4
    photo = FSInputFile(pics['main'])
    caption_text = translation('collection_options_text.change')
    collections, has_next_page, total_pages = await get_collection_list_page(session, current_user, page, page_size)
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text),
                                      reply_markup=get_collection_list_kb(collections, page, has_next_page,
                                                                          'set_active'))
    await callback.answer()

@collection_router.callback_query(F.data.startswith('show_collections_list:'))
async def show_collection_list_page(callback: CallbackQuery, current_user: User,
                                    translation, session: AsyncSession):
    page_size = 4
    page = callback.data.split(':')[1]

    if not page:
        page = 1
    else:
        page = int(page)

    offset = (page - 1) * page_size

    collections, has_next_page, total_pages = await get_collection_list_page(session, current_user, page, page_size)

    text_parts = [translation('collections_list_text.collection')]
    for col, count in collections:
        text_parts.append(translation('collections_list_text.sample', collection_name=safe_md(col.name),
                                                                       number=count))

    collection_list = '\n'.join(text_parts)

    # caption_text = f'Page {page}/{total_pages}\n\n{collection_list}'
    caption_text = translation('collections_list_text.list_msg', page=page, total_pages=total_pages,
                               collection_list=collection_list)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['list']),
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_collection_list_kb(collections, page, has_next_page, 'manage'))
    await callback.answer()

@collection_router.callback_query(CollectionsCb.filter(F.action.startswith('manage')))
async def manage_collection(callback: CallbackQuery, callback_data: CollectionsCb,
                            current_user: User, session: AsyncSession):

    collection = await get_collection_by_id(session, callback_data.collection_id)
    photo = FSInputFile(pics['adding'])
    caption_text = f'Choose action for collection *{safe_md(collection.name)}*'
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=manage_collection_options_kb(callback_data.collection_id, collection.name,
                                                                                callback_data.page, current_user))

@collection_router.callback_query(CollectionsCb.filter(F.action == 'set_active'))
async def change_active_collection(callback: CallbackQuery, callback_data: CollectionsCb,
                                   current_user: User, active_collection: Collection,
                                   session: AsyncSession):

    requested_collection_id = callback_data.collection_id
    if active_collection.collection_id == requested_collection_id:
        await callback.answer('This is your current active collection', show_alert=True)
        return
    await set_active_collection(session, current_user.id, requested_collection_id)
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                            caption='Your active collection has been changed',
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=successfully_change_active_collection_kb(callback_data.page))
    await callback.answer()

@collection_router.callback_query(CollectionsCb.filter(F.action == 'delete_collection'))
async def delete_collection_request(callback: CallbackQuery, callback_data: CollectionsCb, session: AsyncSession):
    collection = await get_collection_by_id(session, callback_data.collection_id)
    caption_text = (f'Are you sure you want to delete the *{safe_md(collection.name)}* collection?'
                    f'Please note that all recipes from this collection will also be removed')
    await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['adding']),
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_collection_delete_confirmation_kb(callback_data.page,
                                                                                         callback_data.collection_id))


@collection_router.callback_query(CollectionsCb.filter(F.action == 'confirmed_collection_deletion'))
async def delete_collection_request(callback: CallbackQuery, callback_data: CollectionsCb,
                                    session: AsyncSession, current_user: User,
                                    base_collection_id, active_collection):
    print(f'ACTIVE COLLECTION IS {active_collection.name} | {active_collection.collection_id}')
    is_deleted = False
    requested_collection_id = callback_data.collection_id
    if requested_collection_id == base_collection_id:
        await callback.answer(f'Sorry, you can not delete your base collection.')
        return

    if requested_collection_id == active_collection.collection_id:
        await set_active_collection(session, current_user.id, base_collection_id)

    is_deleted = await delete_collection(session, current_user.id, requested_collection_id, base_collection_id)

    if is_deleted:
        photo = FSInputFile(pics['adding'])
        caption_text = 'Collection has been *deleted*'
    else:
        photo = FSInputFile(pics['adding'])
        caption_text = ('Sorry, there was an error deleting the collection\\. '
                        'The collection *was _not_ deleted*\\. '
                        'Please contact us via feedback to resolve the issue\\.'
                        '\\(please include the name of the collection you were unable to delete\\)')

    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=successfully_change_active_collection_kb(callback_data.page))
    await callback.answer()

@collection_router.callback_query(CollectionsCb.filter(F.action == 'rename_collection'))
async def get_new_collection_name(callback: CallbackQuery, callback_data: CollectionsCb, state: FSMContext):
    photo = FSInputFile(pics['adding'])
    caption_text = 'Write new name for collection'
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text))
    await state.update_data(collection_id_to_rename=callback_data.collection_id,
                            collection_page=callback_data.page)
    await state.set_state(RenameCollection.waiting_new_collection_name)
    await callback.answer()

@collection_router.message(RenameCollection.waiting_new_collection_name)
async def change_collection_name(message: Message, current_user: User, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    collection_id = data.get('collection_id_to_rename')
    page = data.get('collection_page')

    is_change = await rename_collection(session, collection_id, current_user.id, message.text)

    if is_change:
        photo = FSInputFile(pics['adding'])
        caption_text = 'The collection has been successfully renamed'
    else:
        photo = FSInputFile(pics['adding'])
        caption_text = ("Sorry, we couldn\\'t rename the collection. Please send us feedback with the collection name, "
                        "and we'll look into it")

    await message.answer_photo(photo=photo,
                               caption=caption_text,
                               reply_markup=successfully_change_active_collection_kb(page))

    await state.clear()

@collection_router.callback_query(CollectionsCb.filter(F.action == 'show_collection_recipe'))
async def collection_recipes(callback: CallbackQuery, callback_data: CollectionsCb, session: AsyncSession):
    await callback.answer('This feature will be added soon. For now, change your collection to view recipes.')