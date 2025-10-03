from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_btn(translation):
    return InlineKeyboardButton(text=translation('main_menu_btn.main_menu'), callback_data='main_menu')

def get_yes_no_kb(cb_class, yes_action, no_action, obj_id, translation, page=1):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('answers.yes'), callback_data=cb_class(action=yes_action,
                                                                                      page=page,
                                                                                      obj_id=obj_id).pack())],
        [InlineKeyboardButton(text=translation('answers.no'), callback_data=cb_class(action=no_action,
                                                                                     page=page,
                                                                                     obj_id=obj_id).pack())]])