import secrets
from dataclasses import dataclass
from flask import request, make_response, Response, jsonify
from jwt import decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError, InvalidHash

from app.models.user_model import UserModel
from app.utils.constant import * 
_secret = secrets.token_urlsafe(32)


@dataclass
class User:
    """Model for User to facilitate JWT state transfer"""
    username: str


def get_secret():
    return _secret


def get_hash(password: str):
    ph = PasswordHasher()
    print(ph.hash(password))
    return ph.hash(password)


def check_hash(password: str, hash: str) -> bool:
    ph = PasswordHasher()
    try:
        return ph.verify(hash, password)

    except (VerificationError, VerifyMismatchError, InvalidHash):
        return False


def require_jwt(f):
    def wrapper(*args, **kwargs):
        try:
            jwt_cookie = request.cookies.get("auth_jwt")
            jwt = decode(jwt_cookie, get_secret(), algorithms=["HS256"])

        except ExpiredSignatureError:
            resp = make_response()
            resp.status_code = 401
            return Response(status=401, response="JWT expired")

        except (InvalidSignatureError, DecodeError):
            return Response(status=401, response="Invalid JWT")
        
        return f(user=User(username=jwt.get("username")), *args, **kwargs)
    # Renaming the function name:
    wrapper.__name__ = f.__name__
    return wrapper

# Integrate JWT validation and user validation
def require_login(f):
    def wrapper(*args, **kwargs):
        try:
            jwt_cookie = request.cookies.get("auth_jwt")
            jwt = decode(jwt_cookie, get_secret(), algorithms=["HS256"])

            # user validation
            if UserModel.objects(username=jwt.get("username")).first() is None:
                return UNAUTHORIZED

        except ExpiredSignatureError:
            resp = make_response()
            resp.status_code = 401
            return Response(status=401, response="JWT expired")

        except (InvalidSignatureError, DecodeError):
            return Response(status=401, response="Invalid JWT")
        
        return f(user=User(username=jwt.get("username")), *args, **kwargs)
    # Renaming the function name:
    wrapper.__name__ = f.__name__
    return wrapper

def set_cookie_response(response, cookie_name, cookie_value):
    response = make_response(response)
    response.set_cookie(
        key=cookie_name,
        value=cookie_value,
    )

    return response