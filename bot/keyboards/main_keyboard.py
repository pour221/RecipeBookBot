from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import RecipeListCb
# from bot.services.translator import t

# main_menu_btn = InlineKeyboardButton(text='>> Main menu <<', callback_data='main_menu')

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Recipes list', callback_data=RecipeListCb(action='list_page',
                                                                          page=1).pack())],
    [InlineKeyboardButton(text='Add new recipe', callback_data='new_recipe')],
    [InlineKeyboardButton(text='Find recipe', callback_data='find'),
     InlineKeyboardButton(text='Random recipe', callback_data='random')],
    [InlineKeyboardButton(text='My collections', callback_data='my_collections'),
     InlineKeyboardButton(text='Change of collection', callback_data='quick_change_collection')],
    [InlineKeyboardButton(text='Help', callback_data='help'),
     InlineKeyboardButton(text='Feedback', callback_data='feedback')],
])

# feedback_kb = InlineKeyboardMarkup(inline_keyboard=[[main_menu_btn]])
#
# language_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='🇷🇺 Русский', callback_data='language:ru')],
#     [InlineKeyboardButton(text='🇬🇧 English', callback_data='language:en')],
#     [main_menu_btn]
# ])

def get_main_menu_btn(translation):
    return InlineKeyboardButton(text=translation('main_menu_btn.main_menu'), callback_data='main_menu')

def get_feedback_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[[get_main_menu_btn(translation)]])

def get_language_kb(translator):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🇷🇺 Русский', callback_data='language:ru')],
    [InlineKeyboardButton(text='🇬🇧 English', callback_data='language:en')],
    [get_main_menu_btn(translator)]
])

def get_main_menu_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('main_menu_btn.list'), callback_data=RecipeListCb(action='list_page',
                                                                          page=1).pack())],
    [InlineKeyboardButton(text=translation('main_menu_btn.new'), callback_data='new_recipe')],
    [InlineKeyboardButton(text=translation('main_menu_btn.find'), callback_data='find'),
     InlineKeyboardButton(text=translation('main_menu_btn.random'), callback_data='random')],
    [InlineKeyboardButton(text=translation('main_menu_btn.collections'), callback_data='show_collections_list:'),
     InlineKeyboardButton(text=translation('main_menu_btn.change'), callback_data='quick_change_collection')],
    [InlineKeyboardButton(text=translation('main_menu_btn.help'), callback_data='help'),
     InlineKeyboardButton(text=translation('main_menu_btn.feedback'), callback_data='feedback')],
])
