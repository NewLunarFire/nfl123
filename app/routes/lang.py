from app import app
from app.authentication import authenticated
from app.models import User
from app.repositories.user import update_user_lang

from flask import redirect, request


@app.route("/lang/<lang>")
@authenticated()
def change_lang(user: User, lang: str):
    if lang == "en" or lang == "fr":
        update_user_lang(id=user.id, lang=lang)
        app.session.commit()

    return redirect(request.referrer)
