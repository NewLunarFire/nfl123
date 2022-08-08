import re
from flask import render_template, session
from app.dataclasses.user import User
from app.session import Session


def render(template: str, **context) -> str:
    c = get_session_variables()
    c.update(context)
    return render_template(template, **c)


def get_session_variables():
    user = Session(session).get_user()

    return {"logged_in": bool(user), "user": user}
