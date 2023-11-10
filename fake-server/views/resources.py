from flask import request, jsonify
from controllers import controller
from views import app
from .constants import *
from .utils import require_jwt

@app.route("/resources", methods=["GET"])
def get_resources():
    result = controller.get_resources()
    return jsonify(result), 200

@app.route("/resources/<resource_title>/checkout", methods=["POST"])
@require_jwt
def checkout(resource_title, username_from_jwt):
    if not request.is_json:
        return BAD_REQUEST
    data = request.json
    if "project_title" not in data or "amount" not in data:
        return BAD_REQUEST

    project_title = data.get("project_title")
    amount = data.get("amount")

    if not isinstance(amount, int):
        return BAD_REQUEST

    result = controller.checkout(resource_title, project_title, username_from_jwt, amount)
    if not result:
        return BAD_REQUEST
    return NO_CONTENT

@app.route("/resources/<resource_title>/checkin", methods=["POST"])
@require_jwt
def checkin(resource_title, username_from_jwt):
    if not request.is_json:
        return BAD_REQUEST
    data = request.json
    if "project_title" not in data or "amount" not in data:
        return BAD_REQUEST

    project_title = data.get("project_title")
    amount = data.get("amount")

    if not isinstance(amount, int):
        return BAD_REQUEST

    result = controller.checkin(resource_title, project_title, username_from_jwt, amount)
    if not result:
        return BAD_REQUEST
    return NO_CONTENT
