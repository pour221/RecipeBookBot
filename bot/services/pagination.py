from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select, func, and_
from bot.db.models import Collection, Recipe
from bot.keyboards.callbacks import RecipeCb, PaginationCb, CollectionsCb
from bot.keyboards.main_keyboard import get_main_menu_btn
from bot.services.formatting import safe_md


def get_type_config(what: str):
    """
    Return a pagination configuration for a given entity type.

    This function defines how to build callback data, button text,
    pagination callbacks, and bottom buttons for different entities
    (e.g., recipes, collections). It is used by pagination keyboard builders
    to generate inline keyboards dynamically based on the entity type

    :param what: str, The type of entity ("recipe" or "collection")
    :return: dict: A configuration dictionary containing lambdas for
            - "cb": building callback data for list items.
            - "text": defining button text for list items.
            - "back_cb" / "forward_cb": building pagination callbacks.
            - "bottom_btn": creating a bottom navigation button.
    """
    TYPES= {
        "recipe": {
            'cb': lambda obj, page, action, collection_id: RecipeCb(action=action, page=page,
                                                                    obj_id=obj.recipe_id).pack(),
            'text': lambda obj, idx, _: f"{idx}",
            'back_cb': lambda page, collection_id: PaginationCb(action='recipe_page', page=page - 1,
                                                                obj_id=collection_id).pack(),
            'forward_cb': lambda page, collection_id: PaginationCb(action='recipe_page', page=page + 1,
                                                                   obj_id=collection_id).pack(),
            "bottom_btn": lambda t: InlineKeyboardButton(text=t('recipe_list_btm.collections'),
                                                         callback_data=PaginationCb(action='collection_page',
                                                                                    page=1).pack()),
        },
        "collection": {
            'cb': lambda obj, page, action, collection_id: CollectionsCb(action=action, page=page,
                                                                         obj_id=obj.collection_id).pack(),
            'text': lambda obj, idx, _: obj.name.title(),
            'back_cb': lambda page, collection_id: PaginationCb(action='collection_page', page=page-1).pack(),
            'forward_cb': lambda page, collection_id: PaginationCb(action='collection_page', page=page + 1).pack(),
            "bottom_btn": lambda t: InlineKeyboardButton(text=t('collection_menu_btm.create'),
                                                         callback_data='create_collection')
        }
    }
    return TYPES.get(what, {})

def get_pagination_kb(what: str, objects: list, page: int, page_size: int, has_next: bool, translation, num_btn_row=4,
                           collection_id: int | None = None, action: str | None = None):
    """
    Build an inline keyboard for paginated lists

    This function creates a dynamic inline keyboard with list items, pagination controls (previous/next),
    a bottom navigation button (collection list for recipe and create new collection for collection),
    and a main menu button.
    It uses type-specific configuration returned by `get_type_config()` to build callbacks and button texts.

    :param what: str, ("recipe" or "collection")
    :param objects: list, List of database objects to display
    :param page: int, Current page number
    :param page_size: int, Number of items per page
    :param has_next: bool, Whether a next page exists
    :param translation: Callable, A translation function for button texts
    :param num_btn_row: int, optional, Number of buttons per row. Defaults to 4.
    :param collection_id: int | None, optional, ID of the current collection, if applicable.
    :param action: str | None, optional, Action name to encode in callback data.
    :return: InlineKeyboardMarkup, An inline keyboard with paginated list items and navigation controls.
    """
    cfg = get_type_config(what)
    menu_btn = []
    btn_row = []

    for idx, obj in enumerate(objects, start=(page-1) * page_size + 1):
        btn_row.append(InlineKeyboardButton(text=cfg['text'](obj, idx, collection_id),
                                            callback_data=cfg['cb'](obj, page, action, collection_id)))

        if len(btn_row) == num_btn_row:
            menu_btn.append(btn_row)
            btn_row = []

    if btn_row:
        menu_btn.append(btn_row)

    btn_pages = []

    if page > 1:
        btn_pages.append(InlineKeyboardButton(text='<', callback_data=cfg['back_cb'](page, collection_id)))
    if has_next:
        btn_pages.append(InlineKeyboardButton(text='>', callback_data=cfg['forward_cb'](page, collection_id)))

    menu_btn.append(btn_pages)
    menu_btn.append([cfg['bottom_btn'](translation)])
    menu_btn.append([get_main_menu_btn(translation)])

    return InlineKeyboardMarkup(inline_keyboard=menu_btn)


async def get_obj_list(session: AsyncSession, model, user_id: int, where_clause=None, page: int = 1, page_size: int = 10,
                       with_count: bool = False, join_model=None, join_condition=None, count_field=None, search_field=None,
                       search_query: str = None): # TODO:
    """

    :param user_id: int,  current user id
    :param session: AsyncSession — database session
    :param model: SQLAlchemy model
    :param where_clause: filtration condition
    :param page: page Current page number
    :param page_size: number of items per page
    :param with_count: count connect objects (like Recipe for Collection)
    :param join_model: connected model (like Recipe for Collection )
    :param join_condition: join condition
    :param count_field: count field (like Recipe.recipe_id)
    :param search_field:
    :param search_query:
    :return: (items, has_next, total_pages)
    """
    conditions = []

    if where_clause is not None:
        conditions.append(where_clause)
    if search_query and search_field is not None:
        conditions.append(search_field.ilike(f"%{search_query}%"))

    total_stmt = select(func.count()).select_from(model).where(Collection.user_id == user_id)

    if conditions:
        total_stmt = total_stmt.where(and_(*conditions))

    total = await session.scalar(total_stmt)
    total_pages = (total + page_size - 1) // page_size

    if with_count and join_model and count_field and join_condition is not None:
        stmt = (
            select(model, func.count(count_field).label("count"))
            .outerjoin(join_model, join_condition)
            .where(Collection.user_id == user_id)
            .group_by(model.collection_id))
    else:
        stmt = select(model).where(model.user_id == user_id)

    if conditions:
        stmt = stmt.where(and_(*conditions))

    stmt = stmt.limit(page_size + 1).offset((page - 1) * page_size)

    result = await session.execute(stmt)
    rows = result.all()

    if with_count:
        items = [(row[0], row[1]) for row in rows]  # [(Collection, count), ...]
    else:
        items = [row[0] for row in rows]  # [Recipe, Recipe, ...]

    has_next = len(items) > page_size
    return items[:page_size], has_next, total_pages

async def render_recipe_list(session, page, page_size, collection_id, user_id) -> tuple[str, list, bool, int]:
    """
     Render a paginated list of recipes within a specific collection.
    This function queries the database for recipes that belong to the given collection
    and returns:
    - a formatted text representation for displaying to the user (with translations),
    - the list of recipes on the current page,
    - a flag indicating whether there is a next page,
    - and the total number of pages.

    :param session: AsyncSession,
    :param page: int, Current page number
    :param page_size: int, Number of items per page
    :param collection_id: int, collection_id from collections table for requested collection
    :param user_id: int, user_id from users table for current user
    :return: tuple: (str: A formatted text list of recipes, list[Recipe]: A list of Recipe objects for the current page,
                     bool: True if there is a next page available, int: Total number of pages.)
    """
    recipes, has_next, total_pages = await get_obj_list(session, Recipe, user_id, (Recipe.collection_id == collection_id),
                                                        page=page, page_size=page_size)
    recipes_list = '\n'.join([f'{num}. {safe_md(i.recipe_name)}' for num, i in enumerate(recipes, start=(page - 1) * page_size+1)])
    return recipes_list, recipes, has_next, total_pages

async def render_collection_list(session, page, page_size, user_id, translation):
    """
    Render a paginated list of the user's recipe collections with the number of recipes in each.
    This function queries the database for the user's collections with pagination support
    and returns:
    - a formatted text representation for displaying to the user (with translations),
    - the list of collections with the number of recipes in each,
    - a flag indicating whether there is a next page,
    - and the total number of pages.

    :param session: AsyncSession, SQLAlchemy async database session
    :param page: int, Current page number
    :param page_size: int, Number of items per page
    :param user_id: int, user_id from users table for current user
    :param translation: Callable, A translation function used to localize text
    :return:(str: A formatted text list of recipes, list[tuple[Collection, int]]: A list of tuples containing a Collection and its recipe count,
             bool: True if there is a next page available, int: Total number of pages.)
    """
    collections, has_next, total_pages = await get_obj_list(session, model=Collection, user_id=user_id, where_clause=(Collection.user_id == user_id),
                                                            page=page, page_size=page_size, with_count=True, join_model=Recipe,
                                                            join_condition=(Recipe.collection_id == Collection.collection_id),
                                                            count_field=Recipe.recipe_id)

    text_parts = [translation('collections_list_text.collection')]
    for col, count in collections:
        text_parts.append(translation('collections_list_text.sample', collection_name=safe_md(col.name),
                                                                       number=count))

    collection_list = '\n'.join(text_parts)
    return collection_list, collections, has_next, total_pages

async def render_search_recipe_results(session, page, page_size, user_id, query, translation,
                                       scope, active_collection_id):
    """

    :param session:
    :param page:
    :param page_size:
    :param user_id:
    :param query:
    :param where:
    :param translation:
    :param active_collection_id:
    :param where_clause:
    :return:
    """
    if scope == "active_user_collection":
        where_clause = Recipe.collection_id == active_collection_id
    elif scope == "all_user_collections":
        where_clause = Recipe.user_id == user_id
    else:
        where_clause = ''

    results, has_next, total_pages  = await get_obj_list(session, Recipe, user_id, page=page, page_size=page_size,
                                                         where_clause=where_clause, search_query=query,
                                                         search_field=Recipe.recipe_name)
    if not results:
        result_msg = [translation('search_text.unsuccess', query=safe_md(query))]
    else:
        result_msg = [translation('search_text.success', number=len(results))] + [f'{num}\\. {safe_md(recipe.recipe_name)}' for num, recipe in enumerate(results, start=1)]

    return '\n'.join(result_msg), results, has_next, total_pages