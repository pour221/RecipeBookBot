from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.requests.recipe_requests import get_list_page

async def render_recipe_list(session, page, page_size, collection_id) -> tuple[str, list, bool, int]:
    offset = (page - 1) * page_size
    recipes, has_next, total_pages = await get_list_page(session, collection_id, page, page_size)
    recipes_list = '\n'.join([f'{offset + num + 1}. {i.recipe_name}' for num, i in enumerate(recipes)])
    return recipes_list, recipes, has_next, total_pages