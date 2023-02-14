from flask import Blueprint
from app.repositories.user import get_all_users
from app.repositories.match import get_all_matches
from app.utils.rendering import render

health_blueprint = Blueprint("healthcheck", __name__)


@health_blueprint.route("/healthcheck")
def login():
    is_error = False
    error = None
    try:
        get_all_users()
    except Exception as ex:
        is_error = True
        error = ex

    return (
        render("health.html", is_error=is_error, error=error),
        500 if is_error else 200,
    )
