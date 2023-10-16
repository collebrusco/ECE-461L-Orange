from flask import Flask, request, jsonify, json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from bson import ObjectId, json_util
import os
from . import app


# MongoDB connection setup using environment variables
client = MongoClient(
    host=os.getenv("MONGO_HOST_URL", "localhost"),
    port=int(os.getenv("MONGODB_PORT", 27017)),
    username=os.getenv("MONGO_INITDB_ROOT_USERNAME", "myuser"),
    password=os.getenv("MONGO_INITDB_ROOT_PASSWORD", "mypassword"),
    authSource=os.getenv("MONGO_INITDB_DATABASE", "mydatabase")
)

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Successfully connected to MongoDB!")
    db = client['mydatabase']
    print(db.list_collection_names())
    # Now you can perform operations on the database
except Exception as e:
    print("Failed to connect to MongoDB:", str(e))


@app.route('/')
def index():
    # Perform database operations using db object
    # Example: documents = db['mycollection'].find({})
    print(db.list_collection_names())
    return "Hello, MongoDB!"


# def parse_json(data):
#     return json.loads(json_util.dumps(data))

# uri = "mongodb+srv://mimiliao2000:BJygvTTeLo7yALnK@cluster0.n7lh6cn.mongodb.net/?retryWrites=true&w=majority"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
	
# db = client["EE461L-HaaS"]
# users_collection = db["users"]
# resources_collection = db["resources"]
# projects_collection = db["projects"]


# app = Flask(__name__)
# jwt = JWTManager(app)
# app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


# @app.route('/haas/test', methods=["GET"])
# def test():
#     print('call test')
#     return "hello world", 200

# @app.route('/api/v1/projects', methods=["GET"])
# # @jwt_required
# def list_projects():
#     # current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token
#     username = "john_doe"
   
#     # Check if the user exists in the users collection
#     current_user = users_collection.find_one({'username': username},{"project_ids":1})
#     if current_user is None:
#         return jsonify({"msg": "User not found"}), 404

#     # Get list of the projects of the user
#     project_ids = current_user["project_ids"]
#     project_ids_list = list(map(ObjectId, project_ids))

#     # Find projects associated with the current user
#     user_projects = projects_collection.find({'_id': {"$in":project_ids_list}})
#     # Convert MongoDB cursor to list of dictionaries
#     user_projects = list(user_projects)
#     print(user_projects)
#     projects_list = []
#     for project in user_projects:
#         projects_list.append({
#              "project_id": str(project["_id"]),
#              "title": project["title"],
#              "creator": project["user_id"],
#         })
    
#     return parse_json(user_projects), 200

# @app.route('/api/v1/projects', methods=['POST'])
# # @jwt_required  
# def create_project():
#     # TODO: JWT
    
#     try:
#         data = request.get_json()
#         title = data.get('title')
#         description = data.get('description')
#         user_ids = [ObjectId(user_id) for user_id in data.get('user_ids', [])]  # Convert user_ids to ObjectId
#         resources = [{"resource_id": ObjectId(resource.get('resource_id')), "quantity": resource.get('quantity')} for resource in data.get('resources', [])]  # Convert resource_id to ObjectId
#         creator_id = ObjectId(data.get('creator_id'))

#         # TODO: check exist: users, creator, resources
#         # TODO: check resources quantity 

#         # Insert project data into MongoDB collection
#         project_data = {
#             "title": title,
#             "description": description,
#             "user_ids": user_ids,
#             "resources": resources,
#             "creator_id": creator_id
#         }
#         print(project_data)

#         # Inserting the project data into the MongoDB collection
#         result = projects_collection.insert_one(project_data)
#         created_project_id = str(result.inserted_id)

#         # Update user documents with the new project ID
#         for user_id in user_ids + [creator_id]:
#             users_collection.update_one({"_id": ObjectId(user_id)}, {"$addToSet": {"project_ids": ObjectId(created_project_id)}})
        
#         #TODO: resources checkout

#         response = {
#             "message": "Project created successfully",
#             "project_id": created_project_id
#         }
#         return jsonify(response), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/api/v1/projects/<string:project_id>/users', methods=['POST'])
# def add_user_to_project(project_id):
#     try:
#         data = request.get_json()
#         user_id = data.get('user_id')

#         # TODO: Check if the user is already in the projects

#         # Check if the user exists
#         user = users_collection.find_one({"_id": ObjectId(user_id)})
#         if user is None:
#             return jsonify({"error": "User not found"}), 404

#         # Check if the project exists
#         project = projects_collection.find_one({"_id": ObjectId(project_id)})
#         if project is None:
#             return jsonify({"error": "Project not found"}), 404
        
#         # Update the user's project_ids field
#         users_collection.update_one({"_id": ObjectId(user_id)},
#                                     {"$addToSet": {"project_ids": ObjectId(project_id)}})

#         # Add user to the project
#         projects_collection.update_one({"_id": ObjectId(project_id)}, {"$addToSet": {"user_ids": ObjectId(user_id)}})

#         return jsonify({"message": "User added to the project successfully"}), 201

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# if __name__ == '__main__':
# 	app.run(debug=True)
