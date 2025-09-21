from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Find recipe', callback_data='find')],
    [InlineKeyboardButton(text='Random recipe', callback_data='random')],
    [InlineKeyboardButton(text='Recipes list', callback_data='list')],
    [InlineKeyboardButton(text='Add new recipe', callback_data='new_recipe')],
    [InlineKeyboardButton(text='Change collection', callback_data='change'),
     InlineKeyboardButton(text='Create new collection', callback_data='new_collection')],
    [InlineKeyboardButton(text='FeedBack', callback_data='feedback')],
])