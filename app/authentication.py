from app.repositories.user import get_user
from functools import wraps

from flask import session, redirect, url_for


def authenticated(with_user_param=True, require_admin=False):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_id = session.get("user_id")
            user = get_user(id=user_id) if user_id else None

            if not user:
                return redirect(url_for("login"))

            if require_admin:
                if user and not user.is_admin:
                    return redirect("/week")

            if with_user_param:
                return f(user, *args, **kwargs)
            else:
                return f(*args, **kwargs)

        return decorated

    return wrapper
