from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_btn = InlineKeyboardButton(text='>> Main menu <<', callback_data='main_menu')

add_recipes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Quick add', callback_data='quick_add')],
    [InlineKeyboardButton(text='Detailed add', callback_data='detailed_add')],
    [InlineKeyboardButton(text='Generate new recipe with AI', callback_data='ai_generate')],
    [InlineKeyboardButton(text='New options will be here soon', callback_data='new_option')],
    [main_menu_btn]
])


def get_recipe_list_kb(recipes, offset, page: int, has_next: bool) -> InlineKeyboardMarkup:
    recipes_buttons = []
    recipe_row = []
    for idx, recipe in enumerate(recipes, start=1):
        recipe_row.append(InlineKeyboardButton(text=str(offset + idx),
                                               callback_data=f"recipe:{recipe.recipe_id}"))

        if len(recipe_row) == 4:
            recipes_buttons.append(recipe_row)
            recipe_row = []

    if recipe_row:
        recipes_buttons.append(recipe_row)

    page_buttons = []
    if page > 1:
        page_buttons.append(InlineKeyboardButton(text='<', callback_data=f"list_page:{page-1}"))
    if has_next:
        page_buttons.append(InlineKeyboardButton(text='>', callback_data=f"list_page:{page+1}"))

    recipes_buttons.append(page_buttons)
    recipes_buttons.append([main_menu_btn])
    return InlineKeyboardMarkup(inline_keyboard=recipes_buttons)

another_recipe_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Choose another recipe', callback_data='list')],
    [main_menu_btn]
])