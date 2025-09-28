from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto, MessageAutoDeleteTimerChanged
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.handlers.states import FeedbackForm
from bot.utils.formatting import safe_md
from bot.db.requests.recipe_requests import get_list_page
from bot.keyboards.recipes_keyboard import get_recipe_list_kb
from bot.services.main_menu import show_main_menu
from bot.db.requests import init_new_user, change_language
from bot.keyboards.main_keyboard import feedback_kb, language_kb
from bot.keyboards.recipes_keyboard import get_add_recipes_keyboard, get_no_recipe_kb
from bot.keyboards.collections_keyboard import collections_menu_keyboard
from bot.db.models import Collection
from bot.services.translator import get_translation

from data.configs import pics, FEEDBACK_CHAT_ID

main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message, active_collection, translation):
    await show_main_menu(message, translation, active_collection.name)

@main_router.message(Command('cancel'))
async def cancel_command(message: Message, state: FSMContext, active_collection,
                         translation):
    await state.clear()
    await message.answer(translation("command_action.cancel"))
    await show_main_menu(message, translation, active_collection.name)

@main_router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery, state: FSMContext, active_collection, translation):
    await callback.answer()
    await state.clear()
    await show_main_menu(callback, translation, active_collection.name)

@main_router.callback_query(F.data == 'new_recipe')
async def new_recipe(callback: CallbackQuery, translation):
    await callback.answer()
    photo = FSInputFile(pics['new'])
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption=translation('adding_text.menu_text')),
        reply_markup=get_add_recipes_keyboard(translation)
    )

@main_router.callback_query(F.data == 'find')
async def find_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'random')
async def random_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'my_collections')
async def collections_menu(callback: CallbackQuery, translation):
    photo = FSInputFile(pics['main'])
    caption_text = translation('collection_menu_text.collection_prompt')
    await callback.message.edit_media(media=InputMediaPhoto(media=photo,
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=collections_menu_keyboard)
    await callback.answer()


@main_router.callback_query(F.data == 'help')
async def help_msg(callback: CallbackQuery, translation):
    photo = FSInputFile(pics['main'])
    caption_text =translation('help.text')
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=language_kb)

@main_router.callback_query(F.data == 'feedback')
async def get_feedback_from_user(callback: CallbackQuery, translation, state: FSMContext):
    await state.set_state(FeedbackForm.waiting_for_message)
    photo = FSInputFile(pics['adding'])
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
                         reply_markup=feedback_kb)
    await state.clear()

@main_router.callback_query(F.data.startswith('language:'))
async def set_new_language(callback: CallbackQuery, session: AsyncSession, current_user, t,
                        active_collection):
    selected_language = callback.data.split(':')[1]
    await change_language(session, current_user.id, selected_language)
    await session.refresh(active_collection)
    await session.refresh(current_user)

    current_language = current_user.language
    t =  get_translation(current_language)

    await callback.answer()
    await show_main_menu(callback, t, active_collection.name)
