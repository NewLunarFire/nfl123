from flask import Flask, _app_ctx_stack
from app.database import SessionLocal
from sqlalchemy.orm import scoped_session

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
app.secret_key = "patatepoil"

from app import routes
