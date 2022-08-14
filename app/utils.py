from flask import render_template, session, g
from app.repositories.user import get_user

from app.i18n import tr


def render(template: str, **context) -> str:
    sess = get_session()
    ctx = {**context, **sess, "gettext": gettext(sess["lang"])}
    return render_template(template, **ctx)


def get_session():
    user_id = session.get("user_id")
    user = get_user(id=user_id) if user_id else None
    lang = user.lang if user else "en"
    return {"user": user, "lang": lang}

def gettext(lang: str):
    return lambda key: tr(lang, key)

def get_request_time():
    return g.request_time