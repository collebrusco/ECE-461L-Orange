from flask import Flask, request, jsonify, json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId, json_util
from app import app
import os
from urllib.parse import unquote

from .setup_db import users_collection, resources_collection, projects_collection
from .auth import require_jwt, User

def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route('/')
def index():
    return "Welcome to the Flask API!"

@app.route('/projects', methods=["GET"])
@require_jwt
def list_projects(user: User):
    # TODO: JWT
    # username = "user1"
    username = user.username
   
    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': username})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 401

    # Get list of the projects of the user
    project_names = current_user["projects"]

    # Find projects associated with the current user
    user_projects = projects_collection.find({'title': {"$in": project_names}})

    # Convert MongoDB cursor to list of dictionaries
    user_projects = list(user_projects)
    print(user_projects)
    projects_list = []

    # Iterate through the user_projects and fetch users' names and creator's name
    for project in user_projects:
        
        # Create a dictionary for the project with required information
        projects_list.append({
            "title": project["title"],
            "description": project["description"],
            "users": project["users"], # users name
            "creator": project["creator"], # creator name
            "resources": project["resources"],
        })

    
    return parse_json(projects_list), 200

@app.route('/projects', methods=['POST'])
@require_jwt
def create_project(user: User):
    # TODO: JWT
    username = "user1"
    username = user.username
   
    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': username})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 401
    
    # Create a new project
    try:
        data = request.get_json()
        
        # Check if 'title' and 'description' are present in the request JSON
        if 'title' not in data or 'description' not in data:
            return jsonify({"msg": "Title and description are required fields"}), 500
        
        title = data.get('title')
        description = data.get('description')
        
        # Check project title duplicate
        existing_project = projects_collection.find_one({'title': title})
        if existing_project:
            return jsonify({"msg": "Project title already exists"}), 500

        
        users = [] # users not provided
        resources = {"HW Set 1" : 0, "HW Set 2": 0, "HW Set 3": 0} # resources set as default
        # directly frm JWT
        creator = username 

        # Add creator as total users in this project
        users = users + [creator]


        # Insert project data into MongoDB collection
        # TODO: user_ids = 
        project_data = {
            "title": title,
            "description": description,
            "users": users,
            "resources": resources,
            "creator": creator
        }
        print("Project Created: ", project_data)

        # Inserting the project data into the MongoDB collection
        result = projects_collection.insert_one(project_data)
        created_project_id = str(result.inserted_id)

        # Update user documents with the new project Name
        for user in users:
            users_collection.update_one({"username": user}, {"$addToSet": {"projects": title}})
        
        
        response = {
            "msg": "Project created successfully",
            "project_id": created_project_id
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500

 
@app.route('/projects/<string:project_title>/users', methods=['POST'])
@require_jwt
def add_user_to_project(user: User, project_title):
    
    # TODO: JWT
    username = "user1"
    username = user.username

    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': username})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 401


    try:
        # try:
        #     data = request.get_json()
        #     user_add = data.get('user')
        # except:
        user_add = username # username not provided, add yourself
        
        
        # Check if the user exists
        user = users_collection.find_one({"username": user_add})
        if user is None:
            return jsonify({"msg": "User added not found"}), 500

        # Decode the URL parameter (project title)
        project_title = unquote(project_title)

        # Check if the project exists
        project = projects_collection.find_one({"title": project_title})
        if project is None:
            return jsonify({"msg": "Project not found"}), 500

        # Check if the user is already in the project
        if user_add in project.get('users', []):
            return jsonify({"msg": "User is already in the project"}), 500

        # Update the user's projects list
        users_collection.update_one({"username": user_add},
                                    {"$addToSet": {"projects": project["title"]}})

        # Add user to the project
        projects_collection.update_one({"title": project_title}, {"$addToSet": {"users": user_add}})

        return jsonify({"msg": "User added to the project successfully"}), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500



# # TODO: check 
# @app.route('/api/v1/projects/<string:project_id>/users', methods=['DELETE'])
# def remove_user_from_project(project_id):
#     # TODO: JWT
#     # current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token
#     username = "user1"
   
#     # Check if the user exists in the users collection
#     current_user = users_collection.find_one({'username': username},{"project_ids":1})
#     if current_user is None:
#         return jsonify({"msg": "User not found"}), 404
    
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id')
#         # TODO: check whether the user_id and JWT match (requirement: can only add yourself to a project).

#         # Check if the project exists
#         project = projects_collection.find_one({"_id": ObjectId(project_id)})
#         if project is None:
#             return jsonify({"msg": "Project not found"}), 404

#         # Check if the user exists in the project
#         if ObjectId(user_id) not in project.get('user_ids', []):
#             return jsonify({"msg": "User not found in the project"}), 404

#         # Remove user from the project
#         projects_collection.update_one({"_id": ObjectId(project_id)},
#                                        {"$pull": {"user_ids": ObjectId(user_id)}})

#         # Remove project from the user's project_ids field
#         users_collection.update_one({"_id": ObjectId(user_id)},
#                                     {"$pull": {"project_ids": ObjectId(project_id)}})

#         return jsonify({"msg": "User removed from the project successfully"}), 200

#     except Exception as e:
#         return jsonify({"msg": str(e)}), 500
