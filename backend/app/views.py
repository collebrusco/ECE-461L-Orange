from flask import Flask, request, jsonify, json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId, json_util
from app import app
import os
def parse_json(data):
    return json.loads(json_util.dumps(data))

# MongoDB configuration from environment variables
mongo_host = os.getenv("MONGO_HOST")
mongo_port = int(os.getenv("MONGO_PORT"))
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_authdb = os.getenv("MONGO_AUTHDB")
mongo_dbname = os.getenv("MONGO_DB")

client = MongoClient(host=mongo_host, port=mongo_port, username=mongo_username, password=mongo_password, authSource=mongo_authdb)

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Successfully connected to MongoDB!")
    # Now you can perform operations on the database
except Exception as e:
    print("Failed to connect to MongoDB:", str(e))

# Access or create the desired database and collection
db = client[mongo_dbname]
# Create collections
users_collection = db["users"]  
resources_collection = db["resources"]  
projects_collection = db["projects"]  

@app.route('/')
def index():
    return "Welcome to the Flask API!"

@app.route('/initialize-mongodb', methods=['GET'])
def initialize_mongodb():
    # Check if the collection already exists
    if users_collection.find_one():
        return jsonify(message="Collection already initialized."), 200

   # Sample data
    sample_users = [
        {"username": "user1", "password": "password1", "created_at": datetime.now(), "project_ids": []},
        {"username": "user2", "password": "password2", "created_at": datetime.now(), "project_ids": []}
    ]

    sample_resources = [
        {"capacity": 100, "availability": 50, "title": "Resource 1", "type": "Type A", "created_at": datetime.now()},
        {"capacity": 200, "availability": 150, "title": "Resource 2", "type": "Type B", "created_at": datetime.now()}
    ]

    # Insert data into MongoDB collections
    db.resources.insert_many(sample_resources)
    db.users.insert_many(sample_users)

    return jsonify(message="MongoDB collection initialized with sample data."), 201



@app.route('/api/v1/projects', methods=["GET"])
# @jwt_required
def list_projects():
    # TODO: JWT
    # current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token
    username = "user1"
   
    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': username},{"project_ids":1})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 404

    # Get list of the projects of the user
    project_ids = current_user["project_ids"]
    project_ids_list = list(map(ObjectId, project_ids))

    # Find projects associated with the current user
    user_projects = projects_collection.find({'_id': {"$in":project_ids_list}})
    # Convert MongoDB cursor to list of dictionaries
    user_projects = list(user_projects)
    print(user_projects)
    projects_list = []
    for project in user_projects:
        projects_list.append({
             "project_id": str(project["_id"]),
             "title": project["title"],
             "description": project["description"],
             "creator": project["creator_id"],
        })
    
    return parse_json(user_projects), 200

@app.route('/api/v1/projects', methods=['POST'])
# @jwt_required  
def create_project():
    # TODO: JWT
    # current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token
    username = "user1"
   
    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': username},{"project_ids":1})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 404
    
    # Create a new project
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        
        try:
            user_ids = [ObjectId(user_id) for user_id in data.get('user_ids', [])]  # Convert user_ids to ObjectId
        except:
            user_ids = [] # user_ids not provided

        try:
            resources = [{"resource_id": ObjectId(resource.get('resource_id')), "quantity": resource.get('quantity')} for resource in data.get('resources', [])]  # Convert resource_id to ObjectId
        except:
            resources = [] # resources not provided

        # creator_id = ObjectId(data.get('creator_id'))
        # TODO: directly frm JWT
        creator_id = current_user["_id"] 

        # TODO: check exist: users, creator, resources
        # Check if the users and creator exists
        for user_id in user_ids + [creator_id]:
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if user is None:
                return jsonify({"error": "Creator/User ID not found"}), 404
        # TODO: check resources quantity 

        # Insert project data into MongoDB collection
        project_data = {
            "title": title,
            "description": description,
            "user_ids": user_ids,
            "resources": resources,
            "creator_id": creator_id
        }
        print("Project Created: ", project_data)

        # Inserting the project data into the MongoDB collection
        result = projects_collection.insert_one(project_data)
        created_project_id = str(result.inserted_id)

        # Update user documents with the new project ID
        for user_id in user_ids + [creator_id]:
            users_collection.update_one({"_id": ObjectId(user_id)}, {"$addToSet": {"project_ids": ObjectId(created_project_id)}})
        
        #TODO: resources checkout
        
        response = {
            "message": "Project created successfully",
            "project_id": created_project_id
        }
        return jsonify(response), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/projects/<string:project_id>/users', methods=['POST'])
def add_user_to_project(project_id):
    
    # TODO: JWT
    # current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token
    username = "user1"
   
    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': username},{"project_ids":1})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 404


    try:
        data = request.get_json()
        user_id = data.get('user_id')
        # TODO: check whether the user_id and JWT match (requirement: can only add yourself to a project).
        
        # Check if the user exists
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user is None:
            return jsonify({"error": "User not found"}), 404

        # Check if the project exists
        project = projects_collection.find_one({"_id": ObjectId(project_id)})
        if project is None:
            return jsonify({"error": "Project not found"}), 404

        # Check if the user is already in the project
        if ObjectId(user_id) in project.get('user_ids', []):
            return jsonify({"message": "User is already in the project"}), 200

        # Update the user's project_ids field
        users_collection.update_one({"_id": ObjectId(user_id)},
                                    {"$addToSet": {"project_ids": ObjectId(project_id)}})

        # Add user to the project
        projects_collection.update_one({"_id": ObjectId(project_id)}, {"$addToSet": {"user_ids": ObjectId(user_id)}})

        return jsonify({"message": "User added to the project successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# TODO: check 
@app.route('/api/v1/projects/<string:project_id>/users', methods=['DELETE'])
def remove_user_from_project(project_id):
    # TODO: JWT
    # current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token
    username = "user1"
   
    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': username},{"project_ids":1})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 404
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        # TODO: check whether the user_id and JWT match (requirement: can only add yourself to a project).

        # Check if the project exists
        project = projects_collection.find_one({"_id": ObjectId(project_id)})
        if project is None:
            return jsonify({"error": "Project not found"}), 404

        # Check if the user exists in the project
        if ObjectId(user_id) not in project.get('user_ids', []):
            return jsonify({"error": "User not found in the project"}), 404

        # Remove user from the project
        projects_collection.update_one({"_id": ObjectId(project_id)},
                                       {"$pull": {"user_ids": ObjectId(user_id)}})

        # Remove project from the user's project_ids field
        users_collection.update_one({"_id": ObjectId(user_id)},
                                    {"$pull": {"project_ids": ObjectId(project_id)}})

        return jsonify({"message": "User removed from the project successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
