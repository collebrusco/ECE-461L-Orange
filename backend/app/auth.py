import secrets
from dataclasses import dataclass
from flask import request, make_response, Response
from jwt import decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError, InvalidHash
from app import app, client, mongo_authdb

import time
from datetime import datetime, timedelta
from jwt import encode

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

    return wrapper


@app.route('/whoami', methods=['GET'])
@require_jwt
def whoami(user: User):
    return Response(status=200, response=user.username)


@dataclass
class User:
    """Model for User to facilitate JWT state transfer"""
    username: str
