from typing import List

from app import app
from app.models import User


def get_all_users() -> List[User]:
    return app.session.query(User).all()


def get_user(id: int) -> User:
    return app.session.query(User).filter_by(id=id).first()


def get_user_by_name(name: str) -> User:
    return app.session.query(User).filter_by(name=name).first()


def update_user_lang(id: int, lang: str) -> None:
    get_user(id).lang = lang
