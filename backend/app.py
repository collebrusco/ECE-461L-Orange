from flask import Flask, request, jsonify, json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from bson import ObjectId, json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

uri = "mongodb+srv://mimiliao2000:<password>@cluster0.n7lh6cn.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
	
db = client["EE461L-HaaS"]
users_collection = db["users"]
resources_collection = db["resources"]
projects_collection = db["projects"]


app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


@app.route('/haas/test', methods=["GET"])
def test():
    print('call test')
    return "hello world", 200

@app.route('/haas/projects', methods=["GET"])
@jwt_required
def list_all_projects_of_user():
    current_user = get_jwt_identity()  # Get the identity of the current user from the JWT token
    username = "john_doe"
    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': username},{"project_ids":1})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 404
    print(current_user["project_ids"])
    project_ids = current_user["project_ids"]
    project_ids_list = list(map(ObjectId, project_ids))
    # Find projects associated with the current user
    user_projects = projects_collection.find({'_id': {"$in":project_ids_list}})
    print(user_projects[0])
    # Convert MongoDB cursor to list of dictionaries
    projects_list = []
    for project in user_projects:
        # project['_id'] = str(project['_id'])  # Convert ObjectId to string for JSON serialization
        projects_list.append({
             "project_id": str(project["_id"]),
             "title": project["title"],
             "creator": project["user_id"],
        })
    
    return parse_json(projects_list), 200

if __name__ == '__main__':
	app.run(debug=True)
