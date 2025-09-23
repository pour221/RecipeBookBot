from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.main_keyboard import main_menu_btn

collections_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Show my collections', callback_data='show_collections')],
    [InlineKeyboardButton(text='Change active collection', callback_data='change_collection')],
    [InlineKeyboardButton(text='Create new collection', callback_data='create_collection')],
    [InlineKeyboardButton(text='Delete collection', callback_data='delete_collection')],
    [main_menu_btn]
])

successfully_created_collection_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Create another collection', callback_data='create_collection')],
    [InlineKeyboardButton(text='Show my collections', callback_data='show_collections')],
    [main_menu_btn]
])