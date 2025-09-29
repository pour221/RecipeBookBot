from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.callbacks import RecipeCb, RecipeListCb
from bot.keyboards.main_keyboard import get_main_menu_btn

# static variables and keyboards

AVAILABLE_RECIPE_FIELDS = {
    'recipe_name': 'Title',
    'descriptions': 'Description',
    'ingredients_table': 'Ingredients',
    'equipments': 'Equipments',
    'photos': 'Photo'
}

# dynamic keyboards
def get_recipe_list_kb(recipes, offset, page: int, has_next: bool, collection_id: int,
                       translation, collection_list_page=1) -> InlineKeyboardMarkup:
    recipes_buttons = []
    recipe_row = []
    for idx, recipe in enumerate(recipes, start=1):
        recipe_row.append(InlineKeyboardButton(text=str(offset + idx),
                                               callback_data=RecipeCb(action='show_recipe',
                                                                            recipe_id=recipe.recipe_id,
                                                                            page=page).pack()))
        if len(recipe_row) == 4:
            recipes_buttons.append(recipe_row)
            recipe_row = []

    if recipe_row:
        recipes_buttons.append(recipe_row)

    page_buttons = []

    if page > 1:
        page_buttons.append(InlineKeyboardButton(text='<', callback_data=RecipeListCb(action='list_page',
                                                                                      page=page-1,
                                                                                      collection_id=collection_id).pack())) #f"list_page:{page-1}"
    if has_next:
        page_buttons.append(InlineKeyboardButton(text='>', callback_data=RecipeListCb(action='list_page',
                                                                                      page=page+1,
                                                                                      collection_id=collection_id).pack())) #f"list_page:{page+1}"

    recipes_buttons.append(page_buttons)
    recipes_buttons.append([InlineKeyboardButton(text=translation('recipe_list_btm.collections'),
                                                 callback_data=f'show_collections_list:{collection_list_page}')])
    recipes_buttons.append([get_main_menu_btn(translation)])
    return InlineKeyboardMarkup(inline_keyboard=recipes_buttons)

def get_add_recipes_keyboard(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('adding_btm.quick'), callback_data='quick_add')],
    [InlineKeyboardButton(text=translation('adding_btm.detail'), callback_data='detailed_add')],
    [InlineKeyboardButton(text=translation('adding_btm.new_options'), callback_data='new_option')],
    [get_main_menu_btn(translation)]
])
def get_no_recipe_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('adding_btm.quick'), callback_data='quick_add')],
    [InlineKeyboardButton(text=translation('adding_btm.detail'), callback_data='detailed_add')],
    [get_main_menu_btn(translation)]
])

def get_recipe_option_kb(recipe_id: int, page: int, translation) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('recipe_options_btn.choose_recipe'), callback_data=RecipeListCb(action='list_page',
                                                                                                               page=page).pack())], #f'list_page:{page}'

        [InlineKeyboardButton(text=translation('recipe_options_btn.edit'), callback_data=RecipeCb(action='edit_recipe',
                                                                         recipe_id=recipe_id,
                                                                         page=page,).pack()), #f'edit_recipe:{recipe_id}'),
         InlineKeyboardButton(text=translation('recipe_options_btn.delete'), callback_data=RecipeCb(action='delete_recipe',
                                                                           recipe_id=recipe_id,
                                                                           page=page).pack())] ,#f'delete_recipe:{recipe_id}:{page}')

        [get_main_menu_btn(translation)]
])

def get_confirm_delete_kb(recipe_id: int, page: int, translation):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=translation('answers.yes'), callback_data=RecipeCb(action='confirm_delete_recipe',
                                                                              recipe_id=recipe_id,
                                                                              page=page).pack()),#f"confirm_delete_recipe:{recipe_id}:{page}"),
                InlineKeyboardButton(text=translation('answers.no'), callback_data=RecipeCb(action='show_recipe',
                                                                             recipe_id=recipe_id,
                                                                             page=page).pack()) # f"recipe:{recipe_id}:{page}")
            ]
        ]
    )

def successfully_delete_recipe_options(page: int, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('recipe_options_btn.back_to_list'), callback_data=RecipeListCb(action='list_page',
                                                                              page=page).pack())], #f'list_page:{page}')],
        [get_main_menu_btn(translation)]
    ])

def get_edit_options_kb(recipe_id: int, page: int, translation):
    buttons = [[InlineKeyboardButton(text=label,
                                     callback_data=f'edit_field:{field}:{recipe_id}')]
                for field, label in translation('editable_fields').items()]#AVAILABLE_RECIPE_FIELDS.items()
    buttons.append([InlineKeyboardButton(text=translation('recipe_options_btn.back_to_list'), callback_data=RecipeListCb(action='list_page',
                                                                              page=page).pack())])
    buttons.append([get_main_menu_btn(translation)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def successfully_update_recipe_field_options(recipe_id, translation):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translation('recipe_options_btn.edit_another'), callback_data=RecipeCb(action='edit_recipe',
                                                                                       recipe_id=recipe_id).pack())],#f'edit_recipe:{recipe_id}')],
        [InlineKeyboardButton(text=translation('recipe_options_btn.back_to_list'), callback_data=RecipeListCb(action='list_page',
                                                                              page=1).pack())],
        [get_main_menu_btn(translation)]
    ])

def get_successfully_added_recipe_kb(translation):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=translation('successfully_added.quick'), callback_data='quick_add')],
    [InlineKeyboardButton(text=translation('successfully_added.detail'), callback_data='detailed_add')],
    [InlineKeyboardButton(text=translation('successfully_added.to_list'), callback_data=RecipeListCb(action='list_page').pack())],
    [get_main_menu_btn(translation)]
])