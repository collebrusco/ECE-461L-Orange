from mongoengine import *
from datetime import datetime


class UserModel(Document):

    username = StringField(required=True)
    password = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    projects = ListField(StringField())
