from datetime import datetime, timezone
from os import environ

from flask import Flask, g

from app.routes.admin.result import result_blueprint
from app.routes.error import error_blueprint
from app.routes.health import health_blueprint
from app.routes.index import index_blueprint
from app.routes.lang import lang_blueprint
from app.routes.match import match_blueprint
from app.routes.redirect import redirect_routes
from app.routes.standings import standings_blueprint
from app.routes.sw import sw_blueprint
from app.routes.user import user_blueprint
from app.utils.time import to_eastern

app = Flask(__name__)
app.secret_key = "patatepoil"

redirect_url = environ.get("REDIRECT_URL", None)
if redirect_url:
    redirect_routes(app, redirect_url)
else:
    app.register_blueprint(health_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(error_blueprint)
    app.register_blueprint(lang_blueprint)
    app.register_blueprint(match_blueprint)
    app.register_blueprint(standings_blueprint)
    app.register_blueprint(sw_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(result_blueprint)


@app.before_request
def record_request_time():
    g.request_time = datetime.now(timezone.utc)


@app.after_request
def after_request_callback(response):
    g.pop("request_time")
    return response


@app.template_filter()
def to_eastern_time(date_time, granularity="minutes"):
    date_format = "%Y-%m-%d %H:%M"
    if granularity == "seconds":
        date_format = date_format + ":%S"

    return to_eastern(date_time, format=date_format)
