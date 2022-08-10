from app import app
from app.repositories.user import update_user_lang
from app.utils import get_user

from flask import redirect, request, session


@app.route("/lang/<lang>")
def change_lang(lang: str):
    user = get_user()

    if lang == "en" or lang == "fr":
        update_user_lang(id=user.id, lang=lang)
        app.session.commit()
        session["lang"] = lang


    return redirect(request.referrer)
