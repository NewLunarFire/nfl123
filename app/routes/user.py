from app import app
from flask import render_template, session, request
from app.models import User
from app.repositories.user import *
import json


@app.route("/users")
def users():
    users = []
    for user in app.session.query(User).all():
        users.append(user.name)

    return json.dumps(users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        do_login(int(request.form["user"]))

    return render_template("login.html", users=get_all_users(), name=session["user"])


def do_login(id: int):
    user = get_user(id)

    session["user_name"] = user.name
    session["user_id"] = user.id
