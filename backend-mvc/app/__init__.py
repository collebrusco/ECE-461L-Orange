import os

from flask import Flask
from flask_cors import CORS
# from pymongo import MongoClient
from app.views.user_view import user_blueprint
from app.views.project_view import project_blueprint

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(user_blueprint)
app.register_blueprint(project_blueprint)

# DB setup
from mongoengine import *

# MongoDB configuration from environment variables
mongo_host = os.getenv("MONGO_HOST")
mongo_port = int(os.getenv("MONGO_PORT"))
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_authdb = os.getenv("MONGO_AUTHDB")
mongo_dbname = os.getenv("MONGO_DB")

connect(mongo_dbname, 
        host=mongo_host, 
        port=mongo_port, 
        username=mongo_username, 
        password=mongo_password, 
        authSource=mongo_authdb)
