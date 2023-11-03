from flask import Flask, jsonify, request, Response, make_response

from app import app, client, mongo_authdb

client = client
# Access or create the desired database and collection
db = client[mongo_authdb]
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
