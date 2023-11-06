import secrets
from dataclasses import dataclass
from flask import request, make_response, Response
from jwt import decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError, InvalidHash

from app import app
from .setup_db import client, mongo_dbname


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
    # Renaming the function name:
    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:  # request form wasn't set properly
        return Response(status=400, response="Specify both a username and password")

    # check if user exists
    m = client
    users = m[mongo_dbname]["users"]

    user = users.find_one({"username": username})
    if user is None:
        return Response(status=403, response="Invalid username or password")

    # get hash if they exist
    try:
        password_hash = user["password"]

    except ValueError:
        return Response(status=500, response="Database error")  # we really shouldn't be here, is the db
        # messed up?

    if check_hash(password, password_hash):
        token = encode({"username": username, "exp": datetime.now() + timedelta(hours=24)}, get_secret(),
                       algorithm="HS256")
        resp = make_response("OK")
        resp.status_code = 200
        resp.set_cookie("auth_jwt", token)
        return resp


@app.route('/user', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None or password is None:  # request form wasn't set properly
        return Response(status=400, response="Specify both a username and password")

    m = client
    users = m[mongo_dbname]["users"]

    # check if user with same name has already been registered
    if users.find_one({"username": username}) is not None:
        # there's already a user with this username
        # 409 conflict status code fits here
        return Response(status=409, response="User is already registered")

    # user with this name has not been registered, let's create one
    password_hash = get_hash(password)
    created_at = time.time()

    # insert into users table
    users.insert_one({"username": username, "password": password_hash, "created_at": created_at,
                      "projects": []})

    return Response(status=200)


@app.route('/whoami', methods=['GET'])
@require_jwt
def whoami(user: User):
    return Response(status=200, response=user.username)


@app.route('/logoff', methods=['POST'])
def logoff():
    resp = make_response()
    resp.set_cookie(key="auth_jwt", value="")
    resp.status_code = 200
    resp.response = "OK"
    return resp


@dataclass
class User:
    """Model for User to facilitate JWT state transfer"""
    username: str
