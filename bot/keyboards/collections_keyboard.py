from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import CollectionsCb
from bot.keyboards.main_keyboard import main_menu_btn

collections_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Manage my collections', callback_data='show_collections_list:')],
    # [InlineKeyboardButton(text='Change active collection', callback_data='change_collection')],
    [InlineKeyboardButton(text='Create new collection', callback_data='create_collection')],
    # [InlineKeyboardButton(text='Delete collection', callback_data='delete_collection')],
    [main_menu_btn]
])

successfully_created_collection_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Create another collection', callback_data='create_collection')],
    [InlineKeyboardButton(text='Show my collections', callback_data='show_collections_list:')],
    [main_menu_btn]
])

def get_collection_list_kb(collections, offset, page: int, has_next: bool):
    collections_buttons = []
    collection_row = []

    for collection, num in collections:
        collection_row.append(InlineKeyboardButton(text=collection.name,
                                                         callback_data=CollectionsCb(action=f'manage',
                                                                                     page=page,
                                                                                     collection_id=collection.collection_id,
                                                                                     collection_name=collection.name).pack()))
        if len(collection_row) == 2:
            collections_buttons.append(collection_row)
            collection_row = []

    if collection_row:
        collections_buttons.append(collection_row)

    page_buttons = []

    if page > 1:
        page_buttons.append(InlineKeyboardButton(text='<', callback_data=f"show_collections_list:{page-1}"))
    if has_next:
        page_buttons.append(InlineKeyboardButton(text='>', callback_data=f"show_collections_list:{page+1}"))

    collections_buttons.append(page_buttons)
    collections_buttons.append([main_menu_btn])
    return InlineKeyboardMarkup(inline_keyboard=collections_buttons)

def manage_collection_options_kb(collection_id, collection_name, page, user):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Rename collection', callback_data='1')],
        [InlineKeyboardButton(text=f'Set {collection_name} as active', callback_data='2')],
        [InlineKeyboardButton(text='Show recipes', callback_data='3')],
        [InlineKeyboardButton(text='Delete this collection', callback_data='4')],
        [InlineKeyboardButton(text='>Back to collections<', callback_data=f'show_collections_list:{page}')],
        [main_menu_btn]
    ])