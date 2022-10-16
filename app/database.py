from os import environ

from flask import _app_ctx_stack
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

database: str = environ["DATABASE_URL"]
if database.startswith("postgres://"):
    database = database.replace("postgres://", "postgresql://")

connect_args = {}
if database.startswith("sqlite://"):
    connect_args = {"check_same_thread": False}

engine = create_engine(database, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

Base = declarative_base()
