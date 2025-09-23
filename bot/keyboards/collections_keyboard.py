from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import CollectionsCb
from bot.keyboards.main_keyboard import main_menu_btn

collections_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Show my collections', callback_data='show_collections_list:')],
    [InlineKeyboardButton(text='Change active collection', callback_data='change_collection')],
    [InlineKeyboardButton(text='Create new collection', callback_data='create_collection')],
    [InlineKeyboardButton(text='Delete collection', callback_data='delete_collection')],
    [main_menu_btn]
])

successfully_created_collection_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Create another collection', callback_data='create_collection')],
    [InlineKeyboardButton(text='Show my collections', callback_data='show_collections_list:')],
    [main_menu_btn]
])

def get_collection_list_kb(collections, offset, page: int, has_next: bool):
    # collections_buttons = []
    # for idx, collection in enumerate(collections, start=1):
    #     collections_buttons.append([InlineKeyboardButton(text=collection.name.title(),
    #                                                      callback_data=CollectionsCb())])
    page_buttons = []

    if page > 1:
        page_buttons.append(InlineKeyboardButton(text='<', callback_data=f"show_collections_list:{page-1}"))
    if has_next:
        page_buttons.append(InlineKeyboardButton(text='>', callback_data=f"show_collections_list:{page+1}"))

    return InlineKeyboardMarkup(inline_keyboard=[page_buttons, [main_menu_btn]])