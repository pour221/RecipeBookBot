from aiogram.filters.callback_data import CallbackData

class RecipeActionCb(CallbackData, prefix='recipe'):
    action: str
    recipe_id: int
    page: int | None = None

class PaginationAction(CallbackData, prefix='pagination'):
    what: str
    current_page: int
    next_page: int