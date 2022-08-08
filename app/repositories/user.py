from typing import List

from app import app
from app.models import User


def get_all_users() -> List[User]:
    return app.session.query(User).all()


def get_user(id: int) -> User:
    return app.session.query(User).filter_by(id=id).first()
