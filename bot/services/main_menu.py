from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, CallbackQuery, Message, InputMediaPhoto

from bot.keyboards.main_keyboard import main_menu_kb

from data.configs import pics


async def show_main_menu(event):
    photo = FSInputFile(pics['main'])

    if isinstance(event, Message):
        await event.answer_photo(photo=photo,
                               caption='Main menu of *your recipes book*',
                               reply_markup=main_menu_kb, parse_mode=ParseMode.MARKDOWN_V2)
    elif isinstance(event, CallbackQuery):
        await event.message.edit_media(InputMediaPhoto(media=photo,
                                                       caption='Main menu of *your recipes book*',
                                                       parse_mode=ParseMode.MARKDOWN_V2),
                                       reply_markup=main_menu_kb)