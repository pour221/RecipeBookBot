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
from bot.db.requests import init_new_user
from bot.keyboards.main_keyboard import feedback_kb, language_kb
from bot.keyboards.recipes_keyboard import add_recipes_keyboard, no_recipe_kb
from bot.keyboards.collections_keyboard import collections_menu_keyboard
from bot.db.models import Collection

from data.configs import pics, FEEDBACK_CHAT_ID

main_router = Router()

@main_router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    await init_new_user(session, message.from_user.id,
                           message.from_user.username,
                   f'{message.from_user.first_name} {message.from_user.last_name}',
                          message.from_user.is_premium)

    await show_main_menu(message)

@main_router.message(Command('cancel'))
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Action canceled')
    await show_main_menu(message)

@main_router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await show_main_menu(callback)

@main_router.callback_query(F.data == 'new_recipe')
async def new_recipe(callback: CallbackQuery):
    await callback.answer()
    photo = FSInputFile(pics['new'])
    await callback.message.edit_media(
        media=InputMediaPhoto(media=photo, caption='Choose adding option'),
        reply_markup=add_recipes_keyboard
    )

@main_router.callback_query(F.data == 'list')
async def list_recipe(callback: CallbackQuery, active_collection: Collection, session: AsyncSession):
    page = 1
    page_size = 12
    offset = (page - 1) * page_size

    recipes, has_next, total_pages = await get_list_page(session, active_collection, page, page_size)

    if not recipes:
        await callback.message.edit_media(InputMediaPhoto(media=FSInputFile(pics['list']),
                                                          caption='You do not have any recipes'),
                                          reply_markup=no_recipe_kb)
        await callback.answer()
        return


    recipes_list = '\n'.join([f'{offset + num+1}. {i.recipe_name}' for num, i in enumerate(recipes)])
    caption_text = safe_md(f'{len(recipes)} recipes are displayed. Use the menu to view the rest\n\nPage {page}/{total_pages}\n\n{recipes_list}')
    await callback.message.edit_media(
        media=InputMediaPhoto(media=FSInputFile(pics['list']),
                              caption= caption_text,
                              parse_mode=ParseMode.MARKDOWN_V2),
        reply_markup=get_recipe_list_kb(recipes, offset, page, has_next))
    await callback.answer()

@main_router.callback_query(F.data == 'find')
async def find_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'random')
async def random_recipe(callback: CallbackQuery):
    await callback.answer('Not ready yet')

@main_router.callback_query(F.data == 'my_collections')
async def collections_menu(callback: CallbackQuery, session: AsyncSession):
    photo = FSInputFile(pics['main'])
    caption_text = 'Choose what you want to do'
    await callback.message.edit_media(media=InputMediaPhoto(media=photo,
                                                            caption=caption_text,
                                                            parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=collections_menu_keyboard)
    await callback.answer()


@main_router.callback_query(F.data == 'help')
async def help_msg(callback: CallbackQuery):
    photo = FSInputFile(pics['main'])
    caption_text =('This is Bot to store your favorite recipe\\.\n*This is test description*\n'
                           'Commands:\n'
                           '/start \\- start bot and calling main menu\n'
                           '/cancel \\- cancel current action and return to main menu')
    await callback.message.edit_media(InputMediaPhoto(media=photo,
                                                      caption=caption_text,
                                                      parse_mode=ParseMode.MARKDOWN_V2),
                                      reply_markup=language_kb)

@main_router.callback_query(F.data == 'feedback')
async def get_feedback_from_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FeedbackForm.waiting_for_message)
    photo = FSInputFile(pics['adding'])
    caption_text = ("Write your feedback: Write what you like, what you don't like, what you would like to add, "
                    "and what seems unnecessary and, in your opinion, can be removed.")
    await callback.message.edit_media(media=InputMediaPhoto(media=photo,
                                                            caption=caption_text))
    await callback.answer()

@main_router.message(FeedbackForm.waiting_for_message)
async def receive_feedback(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(FEEDBACK_CHAT_ID,
                           f'Feedback from @{message.from_user.username}\nID: {message.from_user.id}\n\nReceived message:\n{message.text}')
    await message.answer(f"Thank you for your feedback! Your message has been sent, we're working hard to get better!",
                         reply_markup=feedback_kb)
    await state.clear()

@main_router.callback_query(F.data.startswith('language:'))
async def change_language(callback: CallbackQuery, session: AsyncSession):
    selected_language = callback.data.split(':')[1]
    if selected_language == 'ru':
        await callback.answer('Русский язык скоро появится!')
    elif selected_language == 'en':
        await callback.answer('Your current language is English')