from flask import Flask, jsonify
from pymongo import MongoClient
import os
from app import app

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


