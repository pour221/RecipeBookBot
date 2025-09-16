from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class QuickRecipe(StatesGroup):
    name = State()
    description = State()
    photos = State()

class DetailRecipe(StatesGroup):
    name = State()
    ingredients = State()
    description = State()
    equipments = State()
    photos = State()