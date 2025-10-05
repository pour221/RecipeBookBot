from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.states import FeedbackForm
from bot.db.requests import change_language, get_random_recipe
from bot.keyboards.main_keyboard import get_feedback_kb, get_language_kb
from bot.keyboards.recipes_keyboard import get_add_recipes_keyboard, get_random_recipe_kb
from bot.services.formatting import get_translation, safe_md, get_recipe_photo, render_recipe_text
from bot.services.main_menu import show_main_menu

from data.configs import pics, FEEDBACK_CHAT_ID

main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message, active_collection_name: str, translation):
    await show_main_menu(message, translation, active_collection_name)

@main_router.message(Command('cancel'))
async def cancel_command(message: Message, state: FSMContext, active_collection_name,
                         translation):
    await state.clear()
    await message.answer(translation("command_action.cancel"))
    await show_main_menu(message, translation, active_collection_name)

@main_router.message(Command('language'))
async def cancel_command(message: Message):
    await message.answer('Данная команда ловится, но пока не готова')

@main_router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery, state: FSMContext, active_collection_name, translation):
    await callback.answer()
    await state.clear()
    await show_main_menu(callback, translation, active_collection_name)

@main_router.callback_query(F.data.startswith('new_recipe:'))
async def new_recipe(callback: CallbackQuery, current_user, translation):
    if not callback.data.split(':')[1]:
        target_collection = current_user.active_collection_id
    else:
        target_collection = int(callback.data.split(':')[1])

    photo = FSInputFile(pics['new_recipe'])
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption=translation('adding_text.menu_text')),
        reply_markup=get_add_recipes_keyboard(translation, target_collection))
    await callback.answer()

@main_router.callback_query(F.data == 'find')
async def find_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'random')
async def random_recipe(callback: CallbackQuery, current_user, translation, session: AsyncSession):
    recipe = await get_random_recipe(session, current_user.active_collection_id)
    if not recipe:
        await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['empty_list']),
                                                          caption=translation('adding_text.no_recipe')),
                                          reply_markup=get_add_recipes_keyboard(translation, current_user.active_collection_id))
        await callback.answer()
        return

    recipe_msg = render_recipe_text(recipe, translation)
    recipe_photo = FSInputFile(get_recipe_photo(recipe, pics['my_recipe']))
    await callback.message.answer_photo(photo=recipe_photo,
                                        caption=recipe_msg,
                                        parse_mode=ParseMode.MARKDOWN_V2,
                                        reply_markup=get_random_recipe_kb(translation))

    await callback.answer()

@main_router.callback_query(F.data == 'help')
async def help_msg(callback: CallbackQuery, translation):
    photo = FSInputFile(pics['main_menu'])
    caption_text =translation('help.text')
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=get_language_kb(translation))

@main_router.callback_query(F.data == 'feedback')
async def get_feedback_from_user(callback: CallbackQuery, translation, state: FSMContext):
    await state.set_state(FeedbackForm.waiting_for_message)
    photo = FSInputFile(pics['edit'])
    caption_text = translation('feedback.text')
    await callback.message.edit_media(media=InputMediaPhoto(media=photo,
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2))
    await callback.answer()

@main_router.message(FeedbackForm.waiting_for_message)
async def receive_feedback(message: Message, state: FSMContext, translation, bot: Bot):
    await bot.send_message(FEEDBACK_CHAT_ID,
                           text=(f'Feedback from @{message.from_user.username}\nID: {message.from_user.id}\n\n'
                           f'Received message:\n{message.text}'))
    await message.answer(translation('feedback.thanks'),
                         reply_markup=get_feedback_kb(translation))
    await state.clear()

@main_router.callback_query(F.data.startswith('language:'))
async def set_new_language(callback: CallbackQuery, session: AsyncSession, current_user,
                        active_collection_name):
    selected_language = callback.data.split(':')[1]
    await change_language(session, current_user.id, selected_language)
    await session.refresh(current_user)

    current_language = current_user.language
    translation =  get_translation(current_language)

    await callback.answer()
    await show_main_menu(callback, translation, active_collection_name)
