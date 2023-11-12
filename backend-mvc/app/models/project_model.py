from mongoengine import *
from datetime import datetime

class ProjectModel(Document):

    title = StringField(required=True)
    description = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    users = ListField(StringField())
    creator = StringField()
    resources = ListField(DictField())



