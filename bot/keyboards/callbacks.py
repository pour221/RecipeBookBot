from aiogram.filters.callback_data import CallbackData

class BaseCb(CallbackData, prefix='base_callback'):
    action: str | None = None
    page: int = 1
    obj_id: int

class RecipeCb(BaseCb, prefix='recipe'):
    pass

class CollectionsCb(BaseCb, prefix='collection'):
    pass

class PaginationCb(BaseCb, prefix='pagination'):
    action: str
    page: int
    obj_id: int | None = None