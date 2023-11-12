from app.models.user_model import UserModel
from app.models.project_model import ProjectModel

from app.utils.exception import *
from app.utils.constant import * 

class ProjectController:
    @staticmethod
    def get_project_by_username(username):
        
        # find user projects
        user_projects = UserModel.objects(username=username).first().projects
        
        # find projects with project titles
        projects = ProjectModel.objects(title__in=user_projects)
        
       
        return projects
        

    @staticmethod
    def create_project(username, data):

        
        # check project title duplicate
        if ProjectModel.objects(title=data.get('title')).first() is not None:
            raise ConflictError
        
        # create project data
        project_data = {
            "title": data.get('title'),
            "description": data.get('description'),
            "creator": username,
            "users": [username], # members include creator
            "resources": [{resource_type : 0} for resource_type in RESOURCES_SET] # initialize usage to 0
        }
        

        # insert to db
        new_project = ProjectModel(**project_data)
        new_project.save()

        # update user projects
        for user in project_data["users"]:
            query_user = UserModel.objects(username=user).first()
            query_user.projects = query_user.projects + [project_data["title"]]
            query_user.save()

       

        