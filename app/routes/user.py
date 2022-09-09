from flask import Blueprint, redirect, request, session, url_for
from passlib.hash import pbkdf2_sha256

from app.authentication import authenticated
from app.database import Session
from app.models import User
from app.repositories.user import get_user_by_name
from app.utils.rendering import render

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    verification_failed = False

    if request.method == "POST":
        user_id = do_login(request.form["user"], request.form["password"])
        if user_id:
            session["user_id"] = user_id
            return redirect("week")

        verification_failed = True

    return render("login.html", verification_failed=verification_failed)


@user_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("user.login"))


@user_blueprint.route("/profile", methods=["GET", "POST"])
@authenticated()
def profile(user: User):
    is_pw_change: bool = False
    is_success: bool = False
    if request.method == "POST":
        is_pw_change = True
        is_success = do_password_change(user)

    return render("user.html", is_pw_change=is_pw_change, is_success=is_success)


def do_password_change(user: User) -> bool:
    current_password = request.form["current_password"]
    password_new = request.form["password_new"]
    password_bis = request.form["password_bis"]

    if not (current_password and password_new and password_bis):
        return False

    if not pbkdf2_sha256.verify(current_password, user.password):
        return False

    if not password_new == password_bis:
        return False

    user.password = pbkdf2_sha256.hash(password_new)
    Session.commit()
    return True


def do_login(name: str, password: str) -> int:
    user = get_user_by_name(name)

    if not user:
        return None

    if not pbkdf2_sha256.verify(password, user.password):
        return None

    return user.id
