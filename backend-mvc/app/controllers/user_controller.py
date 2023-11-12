from app.models.user_model import UserModel

from app.utils.exception import ConflictError
from app.utils.auth import get_hash
class UserController:
    @staticmethod
    def get_user(username):
        user = UserModel.objects(username=username).first()
        return user

    @staticmethod
    def validate_user(username):
        user = UserModel.objects(username=username).first()
        return user is not None
    
    @staticmethod
    def create_user(username, password):

        # check duplicate username
        if UserController.get_user(username) is not None:
            raise ConflictError
        
        # create new user
        password_hash = get_hash(password)

        user_data = {"username": username,
                      "password": password_hash, 
                      "projects": []}
  
    
        new_user = UserModel(**user_data)
        new_user.save()
