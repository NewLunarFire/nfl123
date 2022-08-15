from flask import Flask, _app_ctx_stack, g
from app.database import SessionLocal
from datetime import datetime
from sqlalchemy.orm import scoped_session


app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
app.secret_key = "patatepoil"


@app.before_request
def record_request_time():
    g.request_time = datetime.now()


@app.after_request
def after_request_callback(response):
    g.pop("request_time")
    return response


from app import routes
