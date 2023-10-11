from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='../build')
CORS(app)
from . import views
