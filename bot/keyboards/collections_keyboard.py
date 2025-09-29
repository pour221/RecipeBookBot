from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import CollectionsCb, RecipeListCb
from bot.keyboards.main_keyboard import get_main_menu_btn

def get_successfully_created_collection_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('collection_options_btm.create_another'), callback_data='create_collection')],
    [InlineKeyboardButton(text=translation('collection_options_btm.show_collections'), callback_data='show_collections_list:')],
    [get_main_menu_btn(translation)]
    ])

def get_collection_list_kb(collections, page: int, has_next: bool, action: str, translation):
    collections_buttons = []
    collection_row = []

    for collection, num in collections:
        collection_row.append(InlineKeyboardButton(text=collection.name,
                                                    callback_data=CollectionsCb(action=action,
                                                                                page=page,
                                                                                collection_id=collection.collection_id).pack()))
        if len(collection_row) == 2:
            collections_buttons.append(collection_row)
            collection_row = []

    if collection_row:
        collections_buttons.append(collection_row)

    page_buttons = []

    if page > 1:
        page_buttons.append(InlineKeyboardButton(text='<', callback_data=f"show_collections_list:{page-1}"))
    if has_next:
        page_buttons.append(InlineKeyboardButton(text='>', callback_data=f"show_collections_list:{page+1}"))

    collections_buttons.append(page_buttons)
    collections_buttons.append([InlineKeyboardButton(text=translation('collection_menu_btm.create'),
                                                     callback_data='create_collection')])
    collections_buttons.append([get_main_menu_btn(translation)])
    return InlineKeyboardMarkup(inline_keyboard=collections_buttons)

def manage_collection_options_kb(collection_id, collection_name, page, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('collection_options_btm.rename'), callback_data=CollectionsCb(action='rename_collection',
                                                                                    collection_id=collection_id,
                                                                                    page=page).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.set', collection_name=collection_name),
                              callback_data=CollectionsCb(action='set_active', collection_id=collection_id,
                                                          page=page).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.show'),
                              callback_data=RecipeListCb(action='list_page', collection_id=collection_id).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.delete'),
                              callback_data=CollectionsCb(action='delete_collection', collection_id=collection_id,
                                                          page=page).pack())],
        [InlineKeyboardButton(text=translation('collection_options_btm.back'), callback_data=f'show_collections_list:{page}')],
        [get_main_menu_btn(translation)]
    ])

def successfully_change_active_collection_kb(page, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('collection_menu_btm.go_to_list'), callback_data=f'show_collections_list:{page}')],
        [InlineKeyboardButton(text=translation('collection_menu_btm.add_new_recipe'), callback_data=f'new_recipe')],
        [InlineKeyboardButton(text=translation('collection_menu_btm.show_recipe'), callback_data=RecipeListCb(action='list_page').pack())],
        [get_main_menu_btn(translation)]
    ])

def get_collection_delete_confirmation_kb(page, collection_id, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('answers.yes'), callback_data=CollectionsCb(action='confirmed_collection_deletion',
                                                                      page=page,
                                                                      collection_id=collection_id).pack())],
        [InlineKeyboardButton(text=translation('answers.no'), callback_data=CollectionsCb(action='manage',
                                                                     page=page,
                                                                     collection_id=collection_id).pack())]
    ])
def successfully_delete_collection_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('collection_menu_btm.go_to_list'), callback_data=f'show_collections_list:')],
        [get_main_menu_btn(translation)]
    ])