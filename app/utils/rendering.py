from flask import render_template, session

from app.i18n import gettext
from app.repositories.user import get_user
from app.utils.time import get_request_time


def render(template: str, **context) -> str:
    sess = get_session()
    util_functions = {
        "gettext": gettext(sess["lang"]),
        "points_color": points_color,
        "score_color": score_color,
    }
    ctx = {**context, **sess, **util_functions}
    return render_template(template, **ctx)


def points_color(points: int) -> str:
    return "green" if points >= 0 else "red"


def score_color(score: int, total: int) -> str:
    if total == 0:
        return "unset"

    pct = score / total
    if pct > 0.6:
        return "green"
    if pct > 0.4:
        return "orange"

    return "red"


def get_session():
    user_id = session.get("user_id")
    user = get_user(user_id=user_id) if user_id else None
    lang = user.lang if user else "en"
    return {"user": user, "lang": lang, "request_time": get_request_time()}
