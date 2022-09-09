from flask import Blueprint
from werkzeug.exceptions import HTTPException

from app.utils.rendering import render

error_blueprint = Blueprint("error", __name__)


@error_blueprint.errorhandler(HTTPException)
def page_not_found(error):
    return render("error.html", error_code=error.code), error.code
