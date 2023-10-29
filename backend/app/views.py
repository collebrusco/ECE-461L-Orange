from flask import Flask, jsonify, request, Response, make_response
from pymongo import MongoClient
import os
import time
from datetime import datetime, timedelta
from jwt import encode

from app import app
from .auth import check_hash, get_hash, get_secret, require_jwt, User

# MongoDB configuration from environment variables
mongo_host = os.getenv("MONGO_HOST")
mongo_port = int(os.getenv("MONGO_PORT"))
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_authdb = os.getenv("MONGO_AUTHDB")
mongo_dbname = os.getenv("MONGO_DB")

client = MongoClient(host=mongo_host, port=mongo_port, username=mongo_username, password=mongo_password,
                     authSource=mongo_authdb)

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Successfully connected to MongoDB!")
    # Now you can perform operations on the database
except Exception as e:
    print("Failed to connect to MongoDB:", str(e))

# Access or create the desired database and collection
db = client[mongo_dbname]
collection = db["test_collection"]


@app.route('/')
def index():
    return "Welcome to the Flask API!"


@app.route('/initialize-mongodb', methods=['GET'])
def initialize_mongodb():
    # Check if the collection already exists
    if collection.find_one():
        return jsonify(message="Collection already initialized."), 200

    # Insert sample data into the collection
    sample_data = [
        {"name": "Item 1", "price": 10.99},
        {"name": "Item 2", "price": 15.49},
        {"name": "Item 3", "price": 7.95}
    ]
    collection.insert_many(sample_data)

    return jsonify(message="MongoDB collection initialized with sample data."), 201


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:  # request form wasn't set properly
        return Response(status=400, response="Specify both a username and password")

    # check if user exists
    m = client
    users = m[mongo_authdb]["users"]

    user = users.find_one({"username": username})
    if user is None:
        return Response(status=403, response="Invalid username or password")

    # get hash if they exist
    try:
        password_hash = user["password"]

    except ValueError:
        return Response(status=500, response="Database error")  # we really shouldn't be here, is the db
        # messed up?

    if check_hash(password, password_hash):
        token = encode({"username": username, "exp": datetime.now() + timedelta(hours=24)}, get_secret(),
                       algorithm="HS256")
        resp = make_response("OK")
        resp.status_code = 200
        resp.set_cookie("auth_jwt", token)
        return resp


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if username is None or password is None:  # request form wasn't set properly
        return Response(status=400, response="Specify both a username and password")

    m = client
    users = m[mongo_authdb]["users"]

    # check if user with same name has already been registered
    if users.find_one({"username": username}) is not None:
        # there's already a user with this username
        # 409 conflict status code fits here
        return Response(status=409, response="User is already registered")

    # user with this name has not been registered, let's create one
    password_hash = get_hash(password)
    created_at = time.time()

    # insert into users table
    users.insert_one({"username": username, "password": password_hash, "created_at": created_at,
                      "project_ids": {}})

    return Response(status=200)


@app.route('/whoami', methods=['GET'])
@require_jwt
def whoami(user: User):
    return Response(status=200, response=user.username)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
