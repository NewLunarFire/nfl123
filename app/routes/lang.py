from flask import Blueprint, redirect, request

from app.authentication import authenticated
from app.database import Session
from app.models import User
from app.repositories.user import update_user_lang

lang_blueprint = Blueprint("lang", __name__)


@lang_blueprint.route("/lang/<lang>")
@authenticated()
def change_lang(user: User, lang: str):
    if lang in {"en", "fr"}:
        update_user_lang(user_id=user.id, lang=lang)
        Session.commit()

    return redirect(request.referrer)
