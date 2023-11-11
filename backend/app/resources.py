import time
from flask import make_response, request, Response, jsonify, json
from app import app
from .setup_db import client, users_collection, resources_collection, projects_collection
from .auth import check_hash, encode, require_jwt, get_hash, User
from bson import json_util

from urllib.parse import unquote
def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/resources', methods=['GET'])
def all_resources():
    resources_list = list(resources_collection.find())
    #for resource in resources_collection:
    #    resources_list.append({
    #        "title": resource["title"],
    #        "availability": resource["availability"],
    #        "capacity": resource["capacity"],
    #    })
    return parse_json(resources_list)
    
@app.route('/resources/<string:resource_title>/checkout', methods=['POST'])
@require_jwt
def checkout(user: User, resource_title):
    # Check to see if user in db
    username =user.username
    user = users_collection.find_one({'username': username})
    if user is None:
        return jsonify({"msg": "User not found"}), 401
    try:
        resource_title = unquote(resource_title)
        if not resource_title:
            return jsonify({"msg": "Malformed request, no resource title"}), 400
        
        # Get our amount from query
        data = request.get_json()
        if "project_title" not in data or "amount" not in data:
            return jsonify({"msg": "project_title and amount are required fields"}), 500
        amount = data.get('amount')
        project = projects_collection.find_one({'title': data.get('project_title')})
        
        # Get our resource
        resource = resources_collection.find_one({"title": resource_title})

        # Check to see if we have specified resource
        if resource is None:
            return jsonify({"msg": "Resource not found"}), 404
        
        # Check to see if we have specified project
        if project is None:
            return jsonify({"msg": "Project not found"}), 404
        
        # Check to see if user has access to project
        if username not in project["users"]:
            return jsonify({'msg': 'User does not have access to project'}), 401
        # If we have enough available to check out 
        if resource["availability"] < amount:
            return jsonify({"msg": "Tried to check out too many"}), 400
        
        resource["availability"] = resource["availability"] - amount
        project["resources"][resource_title] += amount
        # Update Resource in DB
        resources_collection.update_one({"title": resource_title}, {"$set": {"availability": resource["availability"]}})
        projects_collection.update_one({'title': data.get('project_title')}, {"$set": {f"resources.{resource_title}": project["resources"][resource_title]}})
        
        return parse_json(resource), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@app.route('/resources/<string:resource_title>/checkin', methods=['POST'])
@require_jwt
def checkin(user: User, resource_title):
    # Check to see if user in db
    username =user.username
    user = users_collection.find_one({'username': username})
    if user is None:
        return jsonify({"msg": "User not found"}), 401
    try:
        resource_title = unquote(resource_title)
        if not resource_title:
            return jsonify({"msg": "Malformed request, no resource title"}), 400
        
        # Get our amount from query
        data = request.get_json()
        if "project_title" not in data or "amount" not in data:
            return jsonify({"msg": "project_title and amount are required fields"}), 500
        amount = data.get('amount')
        project = projects_collection.find_one({'title': data.get('project_title')})
        
        # Get our resource
        resource = resources_collection.find_one({"title": resource_title})

        # Check to see if we have specified resource
        if resource is None:
            return jsonify({"msg": "Resource not found"}), 404
        
        # Check to see if we have specified project
        if project is None:
            return jsonify({"msg": "Project not found"}), 404
        
        # Check to see if user has access to project
        
        if username not in project["users"]:
            return jsonify({'msg': 'User does not have access to project'}), 401
        
        # If we are not exceeding capacity TODO: Make this if we are not exceeding the amount specified project has checked in
        if resource["capacity"] < amount + resource["availability"]:
            return jsonify({"msg": "Tried to check in too many"}), 400
        if project["resources"][resource_title] < amount:
            return jsonify({"msg": "Tried to check in too many"}), 400
        
        resource["availability"] = resource["availability"] + amount
        project["resources"][resource_title] -= amount
        # Update Resource in DB
        resources_collection.update_one({"title": resource_title}, {"$set": {"availability": resource["availability"]}})
        projects_collection.update_one({'title': data.get('project_title')}, {"$set": {f"resources.{resource_title}": project["resources"][resource_title]}})
        
        return parse_json(resource), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500