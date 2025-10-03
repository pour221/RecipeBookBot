from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import CollectionsCb, PaginationCb
from bot.keyboards.shared_keyboard import get_main_menu_btn

def manage_collection_options_kb(collection_id, collection_name, page, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('collection_menu_btm.add_new_recipe'), callback_data=f'new_recipe:{collection_id}')],
        [InlineKeyboardButton(text=translation('collection_options_btm.rename'), callback_data=CollectionsCb(action='rename_collection',
                                                                                    obj_id=collection_id,
                                                                                    page=page).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.set', collection_name=collection_name),
                              callback_data=CollectionsCb(action='set_active', obj_id=collection_id,
                                                          page=page).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.show'),
                              callback_data=PaginationCb(action='recipe_page', page=1, obj_id=collection_id).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.delete'),
                              callback_data=CollectionsCb(action='delete_collection', obj_id=collection_id,
                                                          page=page).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.back'), callback_data=PaginationCb(action='collection_page',
                                                                                                             page=page).pack())],
        [get_main_menu_btn(translation)]
    ])

# successfully action keyboards
def get_successfully_change_active_collection_kb(page, obj_id, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('collection_menu_btm.go_to_list'), callback_data=PaginationCb(action='collection_page',
                                                                                                             page=page).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.back_to_collection'), callback_data=CollectionsCb(action='manage',
                                                                                                                  page=page,
                                                                                                                  obj_id=obj_id).pack())],
        [InlineKeyboardButton(text=translation('collection_menu_btm.show_recipe'), callback_data=PaginationCb(action='recipe_page',
                                                                                                              page=1,
                                                                                                              obj_id=obj_id).pack())],
        [get_main_menu_btn(translation)]
    ])

def get_successfully_delete_collection_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('collection_menu_btm.go_to_list'), callback_data=PaginationCb(action='collection_page',
                                                                                                             page=1).pack())],
        [get_main_menu_btn(translation)]
    ])

def get_successfully_created_collection_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('collection_options_btm.create_another'), callback_data='create_collection')],
    [InlineKeyboardButton(text=translation('collection_options_btm.show_collections'), callback_data=PaginationCb(action='collection_page',
                                                                                                                  page=1).pack())],
    [get_main_menu_btn(translation)]
    ])
