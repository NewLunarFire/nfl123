from flask import render_template, session
from app.i18n import gettext
from app.repositories.user import get_user
from app.utils.time import get_request_time

def render(template: str, **context) -> str:
    sess = get_session()
    ctx = {**context, **sess, "gettext": gettext(sess["lang"])}
    return render_template(template, **ctx)


def get_session():
    user_id = session.get("user_id")
    user = get_user(id=user_id) if user_id else None
    lang = user.lang if user else "en"
    return {"user": user, "lang": lang, "request_time": get_request_time()}