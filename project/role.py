from functools import wraps
from flask_login import current_user
from flask import current_app
from enum import Enum


class Role(Enum):
    STUDENT = "STUDENT"
    PROFESSOR = "PROFESSOR"
    ADMIN = "ADMIN"


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated():
                return current_app.login_manager.unauthorized()
            urole = current_app.login_manager.reload_user().role
            if ((urole != role) and (role != "ANY")):
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
