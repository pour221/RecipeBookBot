from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

add_recipes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Quick add', callback_data='quick_add')],
    [InlineKeyboardButton(text='Detailed add', callback_data='detailed_add')],
    [InlineKeyboardButton(text='Generate new recipe with AI', callback_data='ai_generate')],
    [InlineKeyboardButton(text='New options will be here soon', callback_data='new_option')],
    [InlineKeyboardButton(text='>> Main menu <<', callback_data='main_menu')]
])