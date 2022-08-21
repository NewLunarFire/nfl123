from app import app
from app.utils.rendering import render
from flask import session, request
from app.repositories.user import get_user_by_name
from flask import redirect, request, session, url_for

from passlib.hash import pbkdf2_sha256


@app.route("/login", methods=["GET", "POST"])
def login():
    verification_failed = False

    if request.method == "POST":
        user_id = do_login(request.form["user"], request.form["password"])
        if user_id:
            session["user_id"] = user_id
            return redirect("week")
        else:
            verification_failed = True

    return render("login.html", verification_failed=verification_failed)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))


def do_login(name: str, password: str) -> int:
    user = get_user_by_name(name)

    if not user:
        return None

    if not pbkdf2_sha256.verify(password, user.password):
        return None

    return user.id
