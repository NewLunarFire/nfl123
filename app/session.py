from app.dataclasses.user import User
from flask.sessions import SessionMixin


class Session:
    user: User

    def __init__(self, session: SessionMixin):
        user_name = session.get("user_name")
        user_id = session.get("user_id")
        if user_name and user_id:
            self.user = User(user_id, user_name)
        else:
            self.user = None

    def get_user(self) -> User:
        return self.user

    def is_logged_in(self) -> bool:
        return bool(self.user)
