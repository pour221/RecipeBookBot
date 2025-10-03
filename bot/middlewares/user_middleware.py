from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User, Collection
from bot.services.formatting import get_translation

class DbUserMiddleware(BaseMiddleware):
   async def __call__(self, handler, event: Message | CallbackQuery, data: dict):

        session:  AsyncSession = data.get('session')

        tg_id = None
        if event.message:
            tg_id = event.message.from_user.id
        elif event.callback_query:
            tg_id = event.callback_query.from_user.id


        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            raise RuntimeError(f"User {tg_id} not found in DB")

        active_collection = await session.get(Collection, user.active_collection_id)
        base_collection = await session.get(Collection, user.user_base_collection_id)

        if not active_collection:
            raise RuntimeError(f"Collection {user.active_collection_id} not found for user {tg_id}")

        data["current_user"] = user
        data["active_collection_name"] = active_collection.name
        data['base_collection_id'] = base_collection.collection_id

        lang = user.language if user.language else 'en'
        data['translation'] = get_translation(lang)

        return await handler(event, data)
