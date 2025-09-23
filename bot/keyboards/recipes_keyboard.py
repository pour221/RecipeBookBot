from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import RecipeActionCb
from bot.keyboards.main_keyboard import main_menu_btn
# static variables and keyboards
AVAILABLE_RECIPE_FIELDS = {
    'recipe_name': 'Title',
    'descriptions': 'Description',
    'ingredients_table': 'Ingredients',
    'equipments': 'Equipments',
    'photos': 'Photo'
}



add_recipes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Quick add', callback_data='quick_add')],
    [InlineKeyboardButton(text='Detailed add', callback_data='detailed_add')],
    [InlineKeyboardButton(text='Generate new recipe with AI', callback_data='ai_generate')],
    [InlineKeyboardButton(text='New options will be here soon', callback_data='new_option')],
    [main_menu_btn]
])

successfully_added_recipe_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Quick add another recipe', callback_data='quick_add')],
    [InlineKeyboardButton(text='Detail add another recipe', callback_data='detailed_add')],
    [InlineKeyboardButton(text='Go to recipe list', callback_data='list')],
    [main_menu_btn]
])

# dynamic keyboards
def get_recipe_list_kb(recipes, offset, page: int, has_next: bool) -> InlineKeyboardMarkup:
    recipes_buttons = []
    recipe_row = []
    for idx, recipe in enumerate(recipes, start=1):
        recipe_row.append(InlineKeyboardButton(text=str(offset + idx),
                                               callback_data=RecipeActionCb(action='show_recipe',
                                                                            recipe_id=recipe.recipe_id,
                                                                            page=page).pack()))
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

def get_recipe_option_kb(recipe_id: int, page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Choose another recipe', callback_data=f'list_page:{page}')],

        [InlineKeyboardButton(text='Edit recipe', callback_data=RecipeActionCb(action='edit_recipe',
                                                                               recipe_id=recipe_id,
                                                                               page=page).pack()), #f'edit_recipe:{recipe_id}'),
         InlineKeyboardButton(text='Delete recipe', callback_data=RecipeActionCb(action='delete_recipe',
                                                                                 recipe_id=recipe_id,
                                                                                 page=page).pack())] ,#f'delete_recipe:{recipe_id}:{page}')

        [main_menu_btn]
])

def get_confirm_delete_kb(recipe_id: int, page: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yes", callback_data=RecipeActionCb(action='confirm_delete_recipe',
                                                                              recipe_id=recipe_id,
                                                                              page=page).pack()),#f"confirm_delete_recipe:{recipe_id}:{page}"),
                InlineKeyboardButton(text="No", callback_data=RecipeActionCb(action='show_recipe',
                                                                             recipe_id=recipe_id,
                                                                             page=page).pack()) # f"recipe:{recipe_id}:{page}")
            ]
        ]
    )

def successfully_delete_recipe_options(page: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Back to list', callback_data=f'list_page:{page}')],
        [main_menu_btn]
    ])

def get_edit_options_kb(recipe_id: int, page: int):
    buttons = [[InlineKeyboardButton(text=label,
                                     callback_data=f'edit_field:{field}:{recipe_id}')]
                for field, label in AVAILABLE_RECIPE_FIELDS.items()]
    buttons.append([InlineKeyboardButton(text='Back to list', callback_data=f'list_page:{page}')])
    buttons.append([main_menu_btn])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def successfully_update_recipe_field_options(recipe_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Edite another field', callback_data=RecipeActionCb(action='edit_recipe',
                                                                                       recipe_id=recipe_id).pack())],#f'edit_recipe:{recipe_id}')],
        [InlineKeyboardButton(text='Back to list', callback_data='list')],
        [main_menu_btn]
    ])