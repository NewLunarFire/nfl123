from app import app
from app.authentication import authenticated
from flask import redirect


@app.route("/")
@authenticated()
def index(user):
    return redirect("/week")
