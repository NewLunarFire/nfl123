from flask import _app_ctx_stack
from sqlalchemy.orm import scoped_session

from app.database import SessionLocal

session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
