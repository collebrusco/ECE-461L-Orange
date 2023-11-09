from flask import request
from .constants import UNAUTHORIZED

def require_jwt(f):
    def wrapper(*args, **kwargs):
        jwt = request.cookies.get("jwt")
        if not jwt:
            return UNAUTHORIZED
        assert "username_from_jwt" not in kwargs
        kwargs["username_from_jwt"] = jwt
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
