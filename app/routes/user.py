from app import app
from app.utils import render
from flask import session, request
from app.repositories.user import get_all_users, get_user
from flask import redirect, request, session, url_for

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        do_login(int(request.form["user"]))
        return redirect("week")

    return render("login.html", users=get_all_users())


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

def do_login(id: int):
    user = get_user(id)
    session["user_id"] = user.id
