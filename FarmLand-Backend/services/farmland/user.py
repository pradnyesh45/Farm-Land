from typing import List, Optional
from helpers.user import UserHelper
from repositories.user import UserRepository
from helpers.api_response import Error, ErrorAdditionalInfo

class UserService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> UserHelper:
        user = UserRepository.authenticate(username, password)
        if not user:
            raise Exception(UserHelper.Errors.INVALID_CREDENTIALS)
        return user

    @staticmethod
    def create_user(user: UserHelper) -> UserHelper:
        user.role = 'User'  # Ensure role is set to User
        return UserRepository.create(user)

    @staticmethod
    def create_admin(user: UserHelper) -> UserHelper:
        user.role = 'Admin'  # Ensure role is set to Admin
        return UserRepository.create(user)

    @staticmethod
    def get_all_users() -> List[UserHelper]:
        return UserRepository.get_all()

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[UserHelper]:
        return UserRepository.get_by_id(user_id)
    
    # Add these methods to the existing UserService class

    @staticmethod
    def create_superuser(user: UserHelper) -> UserHelper:
        user.role = 'SuperUser'  # Ensure role is set to SuperUser
        return UserRepository.create(user)

    @staticmethod
    def get_user_by_username(username: str) -> Optional[UserHelper]:
        return UserRepository.get_by_username(username)
