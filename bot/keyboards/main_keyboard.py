from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_btn = InlineKeyboardButton(text='>> Main menu <<', callback_data='main_menu')

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Recipes list', callback_data='list')],
    [InlineKeyboardButton(text='Add new recipe', callback_data='new_recipe')],
    [InlineKeyboardButton(text='Find recipe', callback_data='find'),
     InlineKeyboardButton(text='Random recipe', callback_data='random')],
    [InlineKeyboardButton(text='My collections', callback_data='my_collections'),
     InlineKeyboardButton(text='Change of collection', callback_data='quick_change_collection')],
    [InlineKeyboardButton(text='Help', callback_data='help'),
     InlineKeyboardButton(text='Feedback', callback_data='feedback')],
])

feedback_kb = InlineKeyboardMarkup(inline_keyboard=[[main_menu_btn]])

language_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇷🇺 Русский', callback_data='language:ru')],
    [InlineKeyboardButton(text='🇬🇧 English', callback_data='language:en')],
    [main_menu_btn]
])
