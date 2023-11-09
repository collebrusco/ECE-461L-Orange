import time
from flask import make_response, request, Response, jsonify
from app import app, client, mongo_authdb
from .setup_db import client, users_collection, resources_collection, projects_collection
from .auth import check_hash, encode, require_jwt, get_hash, User

from urllib.parse import unquote


@app.route('resources', methods=['GET'])
@require_jwt
def all_resources():
    return jsonify(resources_collection)
    
@app.route('resources/<string:resource_title>/checkout', methods='[POST]')
@require_jwt
def checkout(resource_title):
    # if resource_title NULL or not a string
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
        
        # If we have enough available to check out 
        if resource["availability"] < amount:
            return jsonify({"msg": "Tried to check out too many"}), 400
        
        resource["availability"] = resource["availability"] + amount
        project["resources"][resource_title] += amount
        # Update Resource in DB
        resources_collection.update_one({"title": resource_title}, resource)
        projects_collection.update_one({'title': info["project_title"]})
        
        return jsonify(resource), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@app.route('resources/<string:resource_title>/checkin', methods='[POST]')
@require_jwt
def checkin(resource_title):
    # if resource_title NULL or not a string
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
        
        # If we are not exceeding capacity TODO: Make this if we are not exceeding the amount specified project has checked in
        if resource["capacity"] < amount + resource["availability"]:
            return jsonify({"msg": "Tried to check out too many"}), 400
        if project["resources"][resource_title] < amount:
            return jsonify({"msg": "Tried to check out too many"}), 400
        
        resource["availability"] = resource["availability"] + amount
        project["resources"][resource_title] -= amount
        # Update Resource in DB
        resources_collection.update_one({"title": resource_title}, resource)
        projects_collection.update_one({'title': info["project_title"]})
        
        return jsonify(resource), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500