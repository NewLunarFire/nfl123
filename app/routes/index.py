from flask import Blueprint, redirect

from app.authentication import authenticated

index_blueprint = Blueprint("index", __name__)


@index_blueprint.route("/")
@authenticated(with_user_param=False)
def index():
    return redirect("/week")
