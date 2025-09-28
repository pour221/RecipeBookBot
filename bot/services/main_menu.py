from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, CallbackQuery, Message, InputMediaPhoto

from bot.keyboards.main_keyboard import main_menu_kb, get_main_menu_kb
from bot.utils.formatting import safe_md

from data.configs import pics


async def show_main_menu(event, translation, active_collection_name='Base', crutch=False):
    photo = FSInputFile(pics['main'])
    caption_text = translation('main_menu_text.main', collection_name=safe_md(active_collection_name))

    if isinstance(event, Message):
        await event.answer_photo(photo=photo,
                               caption=caption_text,
                               reply_markup=get_main_menu_kb(translation), parse_mode=ParseMode.MARKDOWN_V2)
    elif crutch:
        await event.message.answer_photo(photo=photo,
                               caption=caption_text,
                               reply_markup=get_main_menu_kb(translation), parse_mode=ParseMode.MARKDOWN_V2)
    elif isinstance(event, CallbackQuery):
        await event.message.edit_media(InputMediaPhoto(media=photo,
                                                       caption=caption_text,
                                                       parse_mode=ParseMode.MARKDOWN_V2),
                                       reply_markup=get_main_menu_kb(translation))