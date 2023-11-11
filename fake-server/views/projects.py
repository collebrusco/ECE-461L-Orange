from flask import request, jsonify
from controllers import controller
from views import app
from .constants import *
from .utils import require_jwt

@app.route("/projects", methods=["GET"])
@require_jwt
def get_user_projects(username_from_jwt):
    result = controller.get_user_projects(username_from_jwt)
    print(result)
    return jsonify(result), 200

@app.route("/projects", methods=["POST"])
@require_jwt
def create_project(username_from_jwt):
    if not request.is_json:
        return BAD_REQUEST
    data = request.json
    if "title" not in data or "description" not in data:
        return BAD_REQUEST

    title = data.get("title")
    description = data.get("description")

    result = controller.create_project(title, description, username_from_jwt)
    if not result:
        return BAD_REQUEST
    return jsonify(result), 201

@app.route("/projects/<project_title>/users", methods=["POST"])
@require_jwt
def join_project(project_title, username_from_jwt):
    result = controller.join_project(project_title, username_from_jwt)
    if not result:
        return BAD_REQUEST
    return CREATED
