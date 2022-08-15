from flask import render_template
from app import app
from app.i18n import gettext
from app.utils import render
from werkzeug.exceptions import HTTPException


@app.errorhandler(HTTPException)
def page_not_found(error):
    return render("error.html", error=error.code), error.code
