from typing import List

from black import re
from app import app
from flask import render_template, session, request
from app.models import User
import json


def get_all_users() -> List[User]:
    return app.session.query(User).all()


def get_user(id: int) -> User:
    return app.session.query(User).filter_by(id=id).first()
