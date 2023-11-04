import time
from flask import make_response, request, Response
from app import app, client, mongo_authdb

from .auth import check_hash, encode, require_jwt, get_hash, User


@app.route('users/profile', methods=['PUT'])
@require_jwt
def update_profile(user: User):
    # handle malformed request
    if not request.is_json:
        return Response(status=400, response="Expected application/json request")
    data = request.json
    if "id" not in data.keys:
        return Response(status=400, response="Malformed request")

    # grab user from table
    users = client["users"]
    x = users.find_one({"username": user.username})

    if x is None:
        return Response(status=404, response="User not found")

    # update user
    for key in data.keys:
        if key == "password":
            x[key] = hash(data.get(key))
        else:
            x[key] = data.get(key)

    client["users"].update_one({"username": user.username}, x)
    r = client["users"][user.username]
    del r["password"]
    return Response(status=200, response=r, content_type="application/json")


@app.route('users/profile', methods=['GET'])
@require_jwt
def get_profile(user: User):
    # grab user from table
    users = client["users"]
    x = users.find_one({"username": user.username})

    if x is None:
        return Response(status=404, response="User not found")

    del x["password"]
    return Response(status=200, response=r, content_type="application/json")


@app.route('/user', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None or password is None:  # request form wasn't set properly
        return Response(status=400, response="Specify both a username and password")

    m = client
    users = m[mongo_authdb]["users"]

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
                      "project_ids": {}})

    return Response(status=200)


@app.route('users/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:  # request form wasn't set properly
        return Response(status=400, response="Specify both a username and password")

    # check if user exists
    m = client
    users = m[mongo_authdb]["users"]

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


@app.route('/users/logout', methods=['POST'])
def logout():
    resp = make_response()
    resp.set_cookie(key="auth_jwt", value="")
    resp.status_code = 200
    resp.response = "OK"
    return resp
