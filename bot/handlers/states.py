from aiogram.fsm.state import State, StatesGroup

class QuickRecipe(StatesGroup):
    name = State()
    description = State()

class DetailRecipe(StatesGroup):
    name = State()
    ingredients = State()
    description = State()
    equipments = State()
    photos = State()

class NewCollection(StatesGroup):
    waiting_new_collection_name = State()

# class EditRecipe(StatesGroup):
#     waiting_for_value = State()

class FeedbackForm(StatesGroup):
    waiting_for_message = State()

class RenameCollection(StatesGroup):
    waiting_new_collection_name = State()

class RecipeManage(StatesGroup):
    managing = State()
    waiting_for_value = State()