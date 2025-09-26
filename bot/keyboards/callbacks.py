from aiogram.filters.callback_data import CallbackData

from bot.db.models import Collection

class RecipeCb(CallbackData, prefix='recipe'):
    recipe_id: int
    action: str | None = None
    page: int | None = None

    recipe_name: str | None = None
    description: str | None = None
    ingredient: str | None = None
    equipment: str | None = None

class CollectionsCb(CallbackData, prefix='collection'):
    action: str | None = None
    page : int | None = None
    collection_id: int | None = None


class DbUserCb(CallbackData, prefix='user'):
    user_id: int
    user_current_collection: int


# class DbRecipeCb(CallbackData, prefix='recipe_data'):
#     pass

class PaginationAction(CallbackData, prefix='pagination'):
    what: str
    current_page: int
    next_page: int