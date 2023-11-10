from flask import request, make_response, jsonify
from controllers import controller
from views import app
from .constants import *
from .utils import require_jwt

@app.route("/users", methods=["POST"])
def register():
    if not request.is_json:
        return BAD_REQUEST
    data = request.json
    if "username" not in data or "password" not in data:
        return BAD_REQUEST

    username = data.get("username")
    password = data.get("password")

    result = controller.register(username, password)

    if not result:
        return BAD_REQUEST
    response = make_response(*CREATED)
    response.set_cookie("jwt", result)
    return response

@app.route("/users/login", methods=["POST"])
def login():
    if not request.is_json:
        return BAD_REQUEST
    data = request.json
    if "username" not in data or "password" not in data:
        return BAD_REQUEST

    username = data.get("username")
    password = data.get("password")

    result = controller.login(username, password)

    if not result:
        return BAD_REQUEST
    response = make_response(*NO_CONTENT)
    response.set_cookie("jwt", result)
    return response

@app.route("/users/logout", methods=["POST"])
@require_jwt
def logout(username_from_jwt):
    response = make_response(*NO_CONTENT)
    response.delete_cookie("jwt")
    return response

@app.route("/users/profile", methods=["GET"])
@require_jwt
def get_profile(username_from_jwt):
    result = controller.get_profile(username_from_jwt)
    return jsonify(result), 200
