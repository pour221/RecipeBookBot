from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

EDITABLE_RECIPE_FIELDS = {
    'recipe_name': 'Title',
    'description': 'Description',
    'ingredients_table': 'Ingredients',
    'equipments': 'Equipments',
    'photos': 'Photo'
}

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

def get_recipe_option_kb(recipe_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Choose another recipe', callback_data='list')],

        [InlineKeyboardButton(text='Edit recipe', callback_data=f'edit_recipe:{recipe_id}'),
         InlineKeyboardButton(text='Delete recipe', callback_data=f'delete_recipe:{recipe_id}')],

        [main_menu_btn]
])

def get_confirm_delete_kb(recipe_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes", callback_data=f"confirm_delete_recipe:{recipe_id}"),
                InlineKeyboardButton(text="No", callback_data=f"recipe:{recipe_id}")
            ]
        ]
    )

# def get_edit_methods_kb(recipe_id):
#     return InlineKeyboardMarkup(inline_keyboard=[
#
#         [InlineKeyboardButton(text='Quick edit', callback_data=f'quick_edit:{recipe_id}')],
#         [InlineKeyboardButton(text='Detail edit', callback_data=f'detail_edit:{recipe_id}')],
#         [main_menu_btn]
#
#     ])

def get_edit_options_kb(recipe_id: int):
    # changeable_recipe_attrs = ['name', 'description', 'ingredients_table', 'equipments', 'photos']

    buttons = [[InlineKeyboardButton(text=label,
                                     callback_data=f'edit_field:{field}:{recipe_id}')]
                for field, label in EDITABLE_RECIPE_FIELDS.items()]
    buttons.append([InlineKeyboardButton(text='Back to list', callback_data='list')])
    buttons.append([main_menu_btn])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
    # for recipe_attr in changeable_recipe_attrs:
    #     buttons.append([InlineKeyboardButton(text=recipe_attr.replace('_', ' ').title(),
    #                                          callback_data=f'edit_field:{recipe_attr}:{recipe_id}')])
    #
    # buttons.append([main_menu_btn])
    # return InlineKeyboardMarkup(inline_keyboard=buttons)

def successfully_update_recipe_field_options(recipe_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Edite another field', callback_data=f'edit_recipe:{recipe_id}')],
        [InlineKeyboardButton(text='Back to list', callback_data='list')],
        [main_menu_btn]
    ])