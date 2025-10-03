import json
import os
import re
from pathlib import Path

from data.configs import pics

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOCALES_DIR = os.path.join(BASE_DIR, "locales")

LEXICONS = {}
LANGUAGES = ['en', 'ru']

for language in LANGUAGES:
    with open(f'{LOCALES_DIR}/{language}.json', 'r', encoding='UTF-8') as f:
        LEXICONS[language] = json.load(f)

def get_translation(lang: str):
    def translation(key: str, **kwargs):
        key_components = key.split('.')
        phrases = LEXICONS.get(lang, {})
        if len(key_components) == 1:
            return phrases.get(key_components[0])

        if phrases:
            print('-'*80)
            print(kwargs)
            print(key_components)
            print(phrases.get(key_components[0]).get(key_components[1]))
            print('-' * 80)
            return phrases.get(key_components[0]).get(key_components[1]).format(**kwargs)
        else:
            return key
    return translation

def safe_md(text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def render_recipe_text(recipe, translation):
    parts = [f'*{safe_md(recipe.recipe_name)}*']
    if recipe.ingredients_table:
        parts.append(f'\n{translation('editable_fields.ingredients_table')}: ')
        parts.append(f"{safe_md(recipe.ingredients_table)}")
    if recipe.equipments:
        parts.append(f'\n{translation('editable_fields.equipments')}: ')
        parts.append(f"{safe_md(recipe.equipments)}")
    if recipe.descriptions:
        parts.append(f"{safe_md(recipe.descriptions)}")

    return '\n\n'.join(parts)

def get_recipe_photo(recipe, default_path=pics['my']):
    if recipe.photos and Path(recipe.photos).exists():
        return recipe.photos
    else:
        return default_path