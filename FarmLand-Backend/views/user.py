from flask import Blueprint, request
from services.farmland.user import UserService
from helpers.user import UserHelper
from helpers.api_response import ApiResponse
from utils.api import ApiUtils
from middlewares.auth import authentication_middleware
from helpers.auth import AuthEntityType
from flask_jwt_extended import create_access_token

user_view = Blueprint('user', __name__)

@user_view.route('/auth/login', methods=['POST'])
def login():
    try:
        request_data = request.get_json()
        username = request_data.get('username')
        password = request_data.get('password')
        
        user = UserService.authenticate_user(username, password)
        
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role}
        )

        response_data = {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        }

        api_response = ApiResponse(
            data=response_data,
            msg="Login successful"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@user_view.route('/users', methods=['POST'])
@authentication_middleware(AuthEntityType.ADMIN)
def create_user():
    try:
        request_data = request.get_json()
        user = UserHelper(
            username=request_data['username'],
            password=request_data['password'],
            role='User'  # Will be overwritten by service
        )
        created_user = UserService.create_user(user)
        
        api_response = ApiResponse(
            data={
                'id': created_user.id,
                'username': created_user.username,
                'role': created_user.role
            },
            msg="User created successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@user_view.route('/users/admin', methods=['POST'])
@authentication_middleware(AuthEntityType.SUPER_USER)
def create_admin():
    try:
        request_data = request.get_json()
        user = UserHelper(
            username=request_data['username'],
            password=request_data['password'],
            role='Admin'  # Will be overwritten by service
        )
        created_user = UserService.create_admin(user)
        
        api_response = ApiResponse(
            data={
                'id': created_user.id,
                'username': created_user.username,
                'role': created_user.role
            },
            msg="Admin created successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@user_view.route('/users', methods=['GET'])
@authentication_middleware(AuthEntityType.ADMIN)
def get_all_users():
    try:
        users = UserService.get_all_users()
        user_list = [{
            'id': user.id,
            'username': user.username,
            'role': user.role
        } for user in users]
        
        api_response = ApiResponse(
            data=user_list,
            msg="Users retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@user_view.route('/users/<int:user_id>', methods=['DELETE'])
@authentication_middleware(AuthEntityType.ADMIN)
def delete_user(user_id):
    try:
        UserService.delete_user(user_id)
        
        api_response = ApiResponse(
            data=None,
            msg=f"User with ID {user_id} deleted successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@user_view.route('/users/admin/<int:admin_id>', methods=['DELETE'])
@authentication_middleware(AuthEntityType.SUPER_USER)
def delete_admin(admin_id):
    try:
        UserService.delete_admin(admin_id)
        
        api_response = ApiResponse(
            data=None,
            msg=f"Admin with ID {admin_id} deleted successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)
