from flask import Flask, request, jsonify, json
from pymongo.mongo_client import MongoClient
from datetime import datetime
from bson import ObjectId, json_util
from app import app
import os


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
# Create/Access collections 
users_collection = db["users"]  
resources_collection = db["resources"]  
projects_collection = db["projects"]  

# Initialize resources
sample_resources = [
    {"capacity": 100, "availability": 100, "title": "HW Set 1", "created_at": datetime.now()},
    {"capacity": 200, "availability": 200, "title": "HW Set 2", "created_at": datetime.now()},
    {"capacity": 300, "availability": 300, "title": "HW Set 3", "created_at": datetime.now()}
]
# Check if the collection already exists
if resources_collection.find_one():
    print("Resources collection already initialized.")
else:
    # Insert data into MongoDB collections
    print("Resources collection created.")
    resources_collection.insert_many(sample_resources)

# Initialize mongodb
@app.route('/initialize-mongodb', methods=['GET'])
def initialize_mongodb():
    # Check if the collection already exists
    if users_collection.find_one():
        return jsonify(msg="Collection already initialized."), 200

   # Sample data
    sample_users = [
        # the password is a hashed version of "password1"
        {"username": "user1", "password": '$argon2id$v=19$m=65536,t=3,p=4$9rfKjqg1IIsFNganHXQquw$ozPO5qzrEBq4hCALxmWH6+pXXmyvmon7R1uyKc/dCEI', "created_at": datetime.now(), "projects": []},
        # the password is a hashed version of "password2"
        {"username": "user2", "password": '$argon2id$v=19$m=65536,t=3,p=4$i6gb55DAJ54Ub/RAwxyw2w$2d8mfkSZybD4xoJnw8UrIvs6W3r8u4ad1haYXLQx5gI', "created_at": datetime.now(), "projects": []}
    ]

    sample_resources = [
        {"capacity": 100, "availability": 50, "title": "Resource 1", "created_at": datetime.now()},
        {"capacity": 200, "availability": 150, "title": "Resource 2","created_at": datetime.now()}
    ]

    sample_projects = [
        {"title": "Project 1",
         "description": "This is project 1.",
         "users": ["user1", "user2"],
         "creator": "user1",
         "resources": {"Resource 1" : 3, "Resource 2": 4}}, # title -> quantity
    ]

    # Insert data into MongoDB collections
    db.resources.insert_many(sample_resources)
    db.users.insert_many(sample_users)

    return jsonify(msg="MongoDB collection initialized with sample data."), 201