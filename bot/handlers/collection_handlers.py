from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, MessageAutoDeleteTimerChanged
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests.collection_requests import create_new_collection, get_collection_list_page
from bot.handlers.states import NewCollection
from bot.db.models import User, Collection
from bot.keyboards.collections_keyboard import successfully_created_collection_kb, get_collection_list_kb
from bot.utils.formatting import safe_md

from data.configs import pics

collection_router = Router()

@collection_router.callback_query(F.data == 'create_collection')
async def new_collection(callback: CallbackQuery, state: FSMContext):

    await state.set_state(NewCollection.waiting_new_collection_name)

    photo = FSInputFile(pics['main'])
    caption_text = 'Write name for your new collection.\n\n/cancel - cancel this action'
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text))
    await callback.answer()

@collection_router.message(NewCollection.waiting_new_collection_name)
async def receiving_new_collection_name(message: Message, state: FSMContext,
                                      user: User, session: AsyncSession):
    new_name = message.text
    await create_new_collection(session, user, new_name)
    await state.clear()
    await message.answer_photo(photo=FSInputFile(pics['adding']),
                               caption='A new collection has been created! To use it, change the active collection in the menu.',
                               reply_markup=successfully_created_collection_kb)

@collection_router.callback_query(F.data.startswith('show_collections_list:'))
async def show_collection_list_page(callback: CallbackQuery, user: User, session: AsyncSession):
    page_size = 4
    page = callback.data.split(':')[1]

    if not page:
        page = 1
    else:
        page = int(page)

    offset = (page - 1) * page_size

    collections, has_next_page, total_pages = await get_collection_list_page(session, user, page, page_size)

    collection_list = '\n'.join([f'{offset + num + 1}. {i.name}'
                                 for num, i in enumerate(collections)])
    caption_text = safe_md(f'Page {page}/{total_pages}\n\n{collection_list}')
    await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(pics['list']),
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_collection_list_kb(collections, offset, page, has_next_page))
    await callback.answer()
