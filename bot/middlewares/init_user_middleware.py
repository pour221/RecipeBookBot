from aiogram import BaseMiddleware

from bot.db.requests.user_requests import init_new_user

class InitUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        session = data.get('session')

        from_user_info = None
        if event.message:
            from_user_info = event.message.from_user
        elif event.callback_query:
            from_user_info = event.callback_query.from_user

        if not from_user_info:
            return await handler(event, data)

        tg_id = from_user_info.id
        username = from_user_info.username or False
        fullname = f'{from_user_info.first_name} {from_user_info.last_name}'
        tg_premium = from_user_info.is_premium or False

        await init_new_user(session, tg_id, username, fullname, tg_premium)

        return await handler(event, data)
