import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOCALES_DIR = os.path.join(BASE_DIR, "locales")

LEXICONS = {}
LANGUAGES = ['en', 'ru']

for language in LANGUAGES:
    with open(f'{LOCALES_DIR}/{language}.json', 'r', encoding='UTF-8') as f:
        LEXICONS[language] = json.load(f)

# def t(key: str, lang: str = 'en') -> str:
#     """
#     Get translation using key like "section.key"
#     :param key: str, "section.key"
#     :param lang: "ru" or "en"
#     :return: str
#     """
#
#     key_components = key.split('.')
#     phrases = LEXICONS.get(lang, {})
#
#     if phrases:
#         return phrases.get(key_components[0]).get(key_components[1])
#
#     else:
#         return key

def get_translation(lang: str):
    def translation(key: str, **kwargs):
        key_components = key.split('.')
        phrases = LEXICONS.get(lang, {})
        if not key_components[1]:
            return phrases.get(key_components[0])

        if phrases:
            return phrases.get(key_components[0]).get(key_components[1]).format(**kwargs)
        else:
            return key
    return translation
