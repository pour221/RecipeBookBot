from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests import quick_add_new_recipe, get_recipe_by_number
from bot.handlers.states import QuickRecipe, RecipeListState
from bot.keyboards.recipes_keyboard import another_recipe_kb
from bot.services.main_menu import show_main_menu

from data.configs import pics

recipe_router = Router()

@recipe_router.callback_query(F.data == 'quick_add')
async def quick_add(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(QuickRecipe.name)
    await callback.message.answer('Write recipe title:')

@recipe_router.message(QuickRecipe.name)
async def recipe_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text.title())
    await state.set_state(QuickRecipe.description)
    await message.answer('Write your recipe:')

@recipe_router.message(QuickRecipe.description)
async def recipe_description(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(description=message.text)
    data = await state.get_data()

    await quick_add_new_recipe(session, message.from_user.id, data["name"], data["description"], )
    await message.answer(f'Title: {data["name"]}\nDescription: {data["description"]}')
    await message.answer('Your recipe was add!')
    await state.clear()
    await show_main_menu(message)

@recipe_router.callback_query(F.data == 'detailed_add')
async def quick_add(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@recipe_router.callback_query(F.data == 'ai_generate')
async def quick_add(callback: CallbackQuery):
    await callback.answer('AI not ready right now, sorry. You can try another adding options')

@recipe_router.callback_query(F.data == 'new_option')
async def quick_add(callback: CallbackQuery):
    await callback.answer('New amazing options will be here very soon. Stay tuned!')

@recipe_router.callback_query(F.data == 'pick')
async def pick_recipe_by_number(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(RecipeListState.waiting_for_number)
    await callback.message.answer('Write recipe number')

@recipe_router.message(RecipeListState.waiting_for_number, F.text.regexp(r"^\d+$"))
async def recipe_number(message: Message, state: FSMContext, session: AsyncSession):
    recipe_number = int(message.text)
    recipe = await get_recipe_by_number(session, message.from_user.id, recipe_number)
    if not recipe:
        await message.answer(f"No recipe with number {recipe_number}")
        return

    recipe_msg = f'{recipe.recipe_name.title()}\n\n{recipe.descriptions}'
    photo = FSInputFile(pics['my'])
    await message.answer_photo(photo=photo, caption=recipe_msg, parse_mode=None, reply_markup=another_recipe_kb)
    await state.clear()

