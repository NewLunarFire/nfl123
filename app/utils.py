from flask import render_template, session
from app.dataclasses.user import User

from app.i18n import tr

def render(template: str, **context) -> str:
    sess = get_session()
    ctx = {**context, **sess, "gettext": gettext(sess["lang"])}
    return render_template(template, **ctx)


def get_session():
    user = get_user()
    lang = session.get("lang", "en")
    return {
        "user": user,
        "logged_in": bool(user),
        "lang": lang
    }

def get_user():
    user_name = session.get("user_name")
    user_id = session.get("user_id")

    return User(user_id, user_name) if user_name and user_id else None

def gettext(lang: str):
    return lambda key: tr(lang, key)
    #if lang == "en":

    #return "Patate"
