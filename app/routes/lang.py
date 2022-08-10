from app import app

from flask import redirect, request, session

@app.route("/lang/<lang>")
def change_lang(lang: str):
    if lang == "en" or lang == "fr":
        session["lang"] = lang
    
    return redirect(request.referrer)