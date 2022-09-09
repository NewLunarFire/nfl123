import json


def __load_lang(lang: str):
    with open(f"app/i18n/{lang}.json", encoding="UTF-8") as translations_file:
        return json.load(translations_file)


dictionnaries = {lang: __load_lang(lang) for lang in ["en", "fr"]}


def translate(lang: str, key: str):
    dic = dictionnaries[lang]
    return dic[key] if key in dic else f"??{key}??"


def gettext(lang: str):
    return lambda key: translate(lang, key)
