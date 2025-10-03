import json
import os
import re

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
