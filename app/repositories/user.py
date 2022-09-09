from typing import List

from app.database import Session
from app.models import User


def get_all_users() -> List[User]:
    return Session.query(User).all()


def get_user(user_id: int) -> User:
    return Session.query(User).filter_by(id=user_id).first()


def get_user_by_name(name: str) -> User:
    return Session.query(User).filter_by(name=name).first()


def update_user_lang(user_id: int, lang: str) -> None:
    get_user(user_id).lang = lang
