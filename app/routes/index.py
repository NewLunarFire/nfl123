from app import app
from app.authentication import authenticated
from flask import redirect


@app.route("/")
@authenticated(with_user_param=False)
def index():
    return redirect("/week")
