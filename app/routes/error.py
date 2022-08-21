from app import app
from app.utils.rendering import render
from werkzeug.exceptions import HTTPException


@app.errorhandler(HTTPException)
def page_not_found(error):
    return render("error.html", error_code=error.code), error.code
