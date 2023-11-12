from flask import request, Blueprint
from flask.views import MethodView


from app.controllers.user_controller import UserController
from app.controllers.project_controller import ProjectController

from app.utils.exception import *
from app.utils.auth import * 
from app.utils.constant import * 

project_blueprint = Blueprint('project', __name__)

class ProjectView(MethodView):
    
    decorators = [require_login]

    def get(self, user: User):
        
        # get projects of the user
        projects = ProjectController.get_project_by_username(user.username)

        # Convert the queryset to a list of dictionaries 
        projects_list = [
            {   "title": project.title, 
                "description": project.description,
                "users": project.users,
                "resources": project.resources,
                "creator": project.creator
            } for project in projects]
            
        return projects_list, OK[1]
        

    def post(self, user: User):
        
        # create a new project
        try:
            
            data = request.get_json()
        
            if 'title' not in data or 'description' not in data:
                raise InvalidRequestError
            
            ProjectController.create_project(user.username, data)
            
            return CREATED

            
        except ConflictError as e:
            return CONFLICT  # Conflict

        except InvalidRequestError as e:
            return BAD_REQUEST  # Bad Request

        except Exception as e:
            INTERNAL_SERVER_ERROR[0]["msg"] = str(e)
            return INTERNAL_SERVER_ERROR  # Internal Server Error
        

# register view to blueprint
project_blueprint.add_url_rule('/projects', view_func=ProjectView.as_view('project_view'))
