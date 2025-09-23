from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_btn = InlineKeyboardButton(text='>> Main menu <<', callback_data='main_menu')

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Find recipe', callback_data='find'),
     InlineKeyboardButton(text='Random recipe', callback_data='random')],
    # [InlineKeyboardButton(text='Random recipe', callback_data='random')],
    [InlineKeyboardButton(text='Recipes list', callback_data='list')],
    [InlineKeyboardButton(text='Add new recipe', callback_data='new_recipe')],
    [InlineKeyboardButton(text='My collections', callback_data='my_collections')],
    # [InlineKeyboardButton(text='Change collection', callback_data='change'),
    #  InlineKeyboardButton(text='Create new collection', callback_data='new_collection')],
    [InlineKeyboardButton(text='Help', callback_data='help'),
     InlineKeyboardButton(text='FeedBack', callback_data='feedback')],
])

feedback_kb = InlineKeyboardMarkup(inline_keyboard=[[main_menu_btn]])

language_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇷🇺 Русский', callback_data='language:ru')],
    [InlineKeyboardButton(text='🇬🇧 English', callback_data='language:en')],
    [main_menu_btn]
])