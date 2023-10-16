from flask import Flask, request, jsonify, json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from bson import ObjectId, json_util

def parse_json(data):
    return json.loads(json_util.dumps(data))

uri = "mongodb+srv://mimiliao2000:BJygvTTeLo7yALnK@cluster0.n7lh6cn.mongodb.net/?retryWrites=true&w=majority"

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

@app.route('/api/v1/resource/<string:user_id>', methods=["GET"])
# @jwt_required
def list_resources(user_id):
    
    
   
    # Check if the user exists in the users collection
    current_user = users_collection.find_one({'username': user_id},{"project_ids":1})
    if current_user is None:
        return jsonify({"msg": "User not found"}), 404

    # Get list of the resources of the user
    resource_ids = current_user["resource_id"]
    resource_ids_list = list(map(ObjectId, resource_ids))

    # Find resources associated with the current user
    user_resources = resources_collection.find({'_id': {"$in":resource_ids_list}})
    # Convert MongoDB cursor to list of dictionaries
    user_resources = list(user_resources)
    print(user_resources)
    resources_list = []
    for resource in user_resources:
        resources_list.append({
             "resource_id": str(resource["_id"]),
             "title": resource["title"],
             "capacity": resource["capacity"],
             "availability": resource["availability"],
             "type": resource["type"],
             "created_at": ["created_at"]
        })
    
    return parse_json(user_resources), 200



if __name__ == '__main__':
	app.run(debug=True)