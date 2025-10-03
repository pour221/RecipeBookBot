from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import RecipeCb, PaginationCb
from bot.keyboards.shared_keyboard import get_main_menu_btn

def get_add_recipes_keyboard(translation, collection_id):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('adding_btm.quick'), callback_data=f'quick_add:{collection_id}')],
    [InlineKeyboardButton(text=translation('adding_btm.detail'), callback_data=f'detailed_add:{collection_id}')],
    [InlineKeyboardButton(text=translation('adding_btm.new_options'), callback_data='new_option')],
    [get_main_menu_btn(translation)]
])

def get_recipe_option_kb(recipe_id: int, page: int, translation) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('recipe_options_btn.choose_recipe'), callback_data=PaginationCb(action='recipe_page',
                                                                                                               page=page).pack())],

        [InlineKeyboardButton(text=translation('recipe_options_btn.edit'), callback_data=RecipeCb(action='edit_recipe',
                                                                         obj_id=recipe_id,
                                                                         page=page,).pack()),
         InlineKeyboardButton(text=translation('recipe_options_btn.delete'), callback_data=RecipeCb(action='delete_recipe',
                                                                           obj_id=recipe_id,
                                                                           page=page).pack())],

        [get_main_menu_btn(translation)]
])

def get_edit_options_kb(recipe_id: int, page: int, translation):
    buttons = [[InlineKeyboardButton(text=label,
                                     callback_data=f'edit_field:{field}:{recipe_id}')]
                for field, label in translation('editable_fields').items()]
    buttons.append([InlineKeyboardButton(text=translation('recipe_options_btn.back_to_list'), callback_data=PaginationCb(action='recipe_page',
                                                                              page=page).pack())])
    buttons.append([get_main_menu_btn(translation)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# successfully action keyboards
def get_successfully_delete_recipe_kb(page: int, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('recipe_options_btn.back_to_list'), callback_data=PaginationCb(action='recipe_page',
                                                                              page=page).pack())],
        [get_main_menu_btn(translation)]
    ])

def get_successfully_update_recipe_field_kb(recipe_id, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('recipe_options_btn.edit_another'), callback_data=RecipeCb(action='edit_recipe',
                                                                                       obj_id=recipe_id).pack())],
        [InlineKeyboardButton(text=translation('recipe_options_btn.back_to_list'), callback_data=PaginationCb(action='recipe_page',
                                                                              page=1).pack())],
        [get_main_menu_btn(translation)]
    ])

def get_successfully_added_recipe_kb(translation, collection_id):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('successfully_added.quick'), callback_data=f'quick_add:{collection_id}')],
    [InlineKeyboardButton(text=translation('successfully_added.detail'), callback_data=f'detailed_add:{collection_id}')],
    [InlineKeyboardButton(text=translation('successfully_added.to_list'), callback_data=PaginationCb(action='recipe_page',
                                                                                                     page=1,
                                                                                                     obj_id=collection_id).pack())],
    [get_main_menu_btn(translation)]
])

