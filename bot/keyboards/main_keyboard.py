from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import PaginationCb
from bot.keyboards.shared_keyboard import get_main_menu_btn

def get_main_menu_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('main_menu_btn.list'), callback_data=PaginationCb(action='recipe_page',
                                                                          page=1).pack())],
    [InlineKeyboardButton(text=translation('main_menu_btn.new'), callback_data='new_recipe:')],
    [InlineKeyboardButton(text=translation('main_menu_btn.find'), callback_data='find'),
     InlineKeyboardButton(text=translation('main_menu_btn.random'), callback_data='random')],
    [InlineKeyboardButton(text=translation('main_menu_btn.collections'), callback_data=PaginationCb(action='collection_page',
                                                                                                    page=1).pack()),
     InlineKeyboardButton(text=translation('main_menu_btn.change'), callback_data='quick_change_collection')],
    [InlineKeyboardButton(text=translation('main_menu_btn.help'), callback_data='help'),
     InlineKeyboardButton(text=translation('main_menu_btn.feedback'), callback_data='feedback')],
])

def get_feedback_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[[get_main_menu_btn(translation)]])

def get_language_kb(translator):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇷🇺 Русский', callback_data='language:ru')],
    [InlineKeyboardButton(text='🇬🇧 English', callback_data='language:en')],
    [get_main_menu_btn(translator)]
])