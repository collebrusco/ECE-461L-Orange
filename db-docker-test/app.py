from flask import Flask
from pymongo import MongoClient
import os
app = Flask(__name__)

# MongoDB connection setup using environment variables
client = MongoClient(
    host=os.getenv("MONGODB_HOST", "localhost"),
    port=int(os.getenv("MONGODB_PORT", 27017)),
    username=os.getenv("MONGODB_USERNAME", "myuser"),
    password=os.getenv("MONGODB_PASSWORD", "mypassword"),
    authSource=os.getenv("MONGODB_AUTH_SOURCE", "mydatabase")
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
