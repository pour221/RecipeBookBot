from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_btn = InlineKeyboardButton(text='>> Main menu <<', callback_data='main_menu')

add_recipes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Quick add', callback_data='quick_add')],
    [InlineKeyboardButton(text='Detailed add', callback_data='detailed_add')],
    [InlineKeyboardButton(text='Generate new recipe with AI', callback_data='ai_generate')],
    [InlineKeyboardButton(text='New options will be here soon', callback_data='new_option')],
    [main_menu_btn]
])


def get_scroll_list_kb(page: int, has_next: bool) -> InlineKeyboardMarkup:
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton(text='<', callback_data=f"list_page:{page-1}"))
    if has_next:
        buttons.append(InlineKeyboardButton(text='>', callback_data=f"list_page:{page+1}"))

    return InlineKeyboardMarkup(inline_keyboard=[buttons,
                                                 [InlineKeyboardButton(text='Pick recipe',
                                                                       callback_data='pick')],
                                                 [main_menu_btn]])

# scroll_list_kb = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='<', callback_data='backward_btn'), InlineKeyboardButton(text='>', callback_data='forward_btn')],
#     [main_menu_btn]
# ])

another_recipe_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Choose another recipe', callback_data='list')],
    [main_menu_btn]
])