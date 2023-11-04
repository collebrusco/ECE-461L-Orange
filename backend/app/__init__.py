import os

from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)
from . import project
from . import auth