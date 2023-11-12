from flask import request, Blueprint
from flask.views import MethodView


from app.controllers.user_controller import UserController

from app.utils.exception import ConflictError, InvalidRequestError, UnauthorizedError  
from app.utils.auth import get_secret, check_hash, set_cookie_response
from app.utils.constant import * 

from datetime import datetime, timedelta
from jwt import encode

user_blueprint = Blueprint('user', __name__)
class RegisterView(MethodView):

    def post(self):
        try:
            data = request.get_json()

            if "username" not in data or "password" not in data:
                raise InvalidRequestError

            username = data.get("username")
            password = data.get("password")
            UserController.create_user(username=username, password=password)

            # issue jwt
            token = encode(
                {"username": data.get("username"),  "exp": datetime.now() + timedelta(hours=24)}, 
                get_secret(),
                algorithm="HS256")
            
            response = set_cookie_response(CREATED, "auth_jwt", token)
            return response
        
        except ConflictError as e:
            return CONFLICT  # Conflict

        except InvalidRequestError as e:
            return BAD_REQUEST  # Bad Request

        except Exception as e:
            INTERNAL_SERVER_ERROR[0]["msg"] = str(e)
            return INTERNAL_SERVER_ERROR  # Internal Server Error
        
class LoginView(MethodView):

    def post(self):
        try:
            data = request.get_json()

            if "username" not in data or "password" not in data:
                raise InvalidRequestError

            # get user 
            user = UserController.get_user(data.get("username"))
            if user is None:
                raise UnauthorizedError
            
            # get user password hash
            password = data.get('password')
            password_hash = user.password

            if check_hash(password, password_hash):
                token = encode(
                        {"username": user.username, "exp": datetime.now() + timedelta(hours=24)}, 
                        get_secret(),
                        algorithm="HS256")
                response = set_cookie_response(OK, "auth_jwt", token)
                return response
            else:
                raise UnauthorizedError

        except UnauthorizedError as e:
            return UNAUTHORIZED  
        
        except InvalidRequestError as e:
            return BAD_REQUEST  

        except Exception as e:
            INTERNAL_SERVER_ERROR[0]["msg"] = str(e)
            return INTERNAL_SERVER_ERROR  # Internal Server Error



# register view to blueprint
user_blueprint.add_url_rule('/users', view_func=RegisterView.as_view('register_view'))
user_blueprint.add_url_rule('/users/login', view_func=LoginView.as_view('login_view'))
# user_blueprint.add_url_rule('/users/logout', view_func=LogoutView.as_view('logout_view'))
# user_blueprint.add_url_rule('/users/profile', view_func=ProfileView.as_view('profile_view'))
