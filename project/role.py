from functools import wraps
from flask_login import current_user
from flask import abort
from enum import Enum


class Role(Enum):
    STUDENT = "STUDENT"
    PROFESSOR = "PROFESSOR"
    ADMIN = "ADMIN"


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if role != current_user.role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
