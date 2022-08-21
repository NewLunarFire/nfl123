from flask import Flask, _app_ctx_stack, g
from app.database import SessionLocal
from app.utils.time import to_eastern
from datetime import datetime, timezone
from sqlalchemy.orm import scoped_session

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
app.secret_key = "patatepoil"


@app.before_request
def record_request_time():
    g.request_time = datetime.now(timezone.utc)


@app.after_request
def after_request_callback(response):
    g.pop("request_time")
    return response

@app.template_filter()
def to_eastern_time(dt, granularity="minutes"):
    format = "%Y-%m-%d %H:%M"
    if granularity == "seconds":
        format = format + ":%S"

    return to_eastern(dt, format=format)


from app import routes
