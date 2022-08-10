import json


def __load_lang(lang: str):
    f = open(f"app/i18n/{lang}.json")
    data = json.load(f)
    f.close()
    return data


dictionnaries = {lang: __load_lang(lang) for lang in ["en", "fr"]}


def tr(lang: str, key: str):
    dic = dictionnaries[lang]
    return dic[key] if key in dic else f"??{key}??"
