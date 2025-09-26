from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, CallbackQuery, Message, InputMediaPhoto

from bot.keyboards.main_keyboard import main_menu_kb

from data.configs import pics


async def show_main_menu(event, active_collection_name='Base'):
    photo = FSInputFile(pics['main'])
    caption_text = f'Main menu of *your recipe book*\n\nActive collection is *{active_collection_name}*'

    if isinstance(event, Message):
        await event.answer_photo(photo=photo,
                               caption=caption_text,
                               reply_markup=main_menu_kb, parse_mode=ParseMode.MARKDOWN_V2)
    elif isinstance(event, CallbackQuery):
        await event.message.edit_media(InputMediaPhoto(media=photo,
                                                       caption=caption_text,
                                                       parse_mode=ParseMode.MARKDOWN_V2),
                                       reply_markup=main_menu_kb)