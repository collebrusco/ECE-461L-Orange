import secrets
from dataclasses import dataclass
from flask import request, make_response, Response
from jwt import decode, ExpiredSignatureError, InvalidSignatureError, DecodeError
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError, InvalidHash

import time
from datetime import datetime, timedelta
from jwt import encode

import pytest
import pytest_check as check
import os
from pymongo import MongoClient
import requests

# Table users {
#   id integer [primary key]
#   username varchar
#   password varchar
#   created_at timestamp
#   project_ids list
# }
#  ph.hash('testpass')
# '$argon2id$v=19$m=65536,t=3,p=4$bM4YHke/OkipD3o56/7s3g$Obmg8PyfzD4mn2tcueC4iM0/qWaWLKgfN+EWE7w8i+A'

def initialize_test_user():
    mongo_host = os.getenv("MONGO_HOST")
    mongo_port = int(os.getenv("MONGO_PORT"))
    mongo_username = os.getenv("MONGO_USERNAME")
    mongo_password = os.getenv("MONGO_PASSWORD")
    mongo_authdb = os.getenv("MONGO_AUTHDB")
    mongo_dbname = os.getenv("MONGO_DB")

    client = MongoClient(host=mongo_host, port=mongo_port, username=mongo_username, password=mongo_password,
                         authSource=mongo_authdb)

    try:
        client.admin.command('ismaster')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print("Failed to connect to MongoDB:", str(e))

    db = client[mongo_authdb]
    collection = db["users"]

    if collection.find_one({'username': 'testu'}):
        collection.delete_one({'username': 'testu'})
    test_udata = {"username": "testu", "password": '$argon2id$v=19$m=65536,t=3,p=4$bM4YHke/OkipD3o56/7s3g$Obmg8PyfzD4mn2tcueC4iM0/qWaWLKgfN+EWE7w8i+A', "created_at": datetime.now(), "project_ids": []}
    collection.insert_one(test_udata)


def test_url():
	response = requests.get('http://localhost:8888')
	check.equal(response.status_code, 200)

def test_login_nouser():
	initialize_test_user()
	form = {
	    'username': 'NON-EXISTENT-USER',
	    'password': 'anything',
	}
	response = requests.post('http://localhost:8888/login', data=form)
	check.equal(response.status_code, 403)

def test_login_success():
	initialize_test_user()
	form = {
	    'username': 'testu',
	    'password': 'testpass',
	}
	response = requests.post('http://localhost:8888/login', data=form)
	check.equal(response.status_code, 200)

    
