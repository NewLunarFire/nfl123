from functools import wraps

from flask import redirect, session, url_for

from app.repositories.user import get_user


def authenticated(with_user_param=True, require_admin=False):
    def wrapper(target_function):
        @wraps(target_function)
        def decorated(*args, **kwargs):
            user_id = session.get("user_id")
            user = get_user(user_id=user_id) if user_id else None

            if not user:
                return redirect(url_for("user.login"))

            if require_admin:
                if user and not user.is_admin:
                    return redirect("/week")

            if with_user_param:
                return target_function(user, *args, **kwargs)

            return target_function(*args, **kwargs)

        return decorated

    return wrapper
