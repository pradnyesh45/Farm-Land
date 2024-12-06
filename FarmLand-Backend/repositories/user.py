from typing import Optional, List
from models.user import UserModel
from helpers.user import UserHelper
from mappers.user import UserMapper
from utils.postgres import PostgresUtils
from sqlalchemy.exc import IntegrityError

class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> Optional[UserHelper]:
        user = UserModel.query.get(user_id)
        return UserMapper.to_helper(user) if user else None

    @staticmethod
    def get_by_username(username: str) -> Optional[UserHelper]:
        user = UserModel.query.filter_by(username=username).first()
        return UserMapper.to_helper(user) if user else None

    @staticmethod
    def get_all() -> List[UserHelper]:
        users = UserModel.query.all()
        return UserMapper.to_helper_list(users)

    @staticmethod
    def create(helper: UserHelper) -> UserHelper:
        try:
            model = UserMapper.to_model(helper)
            PostgresUtils.db.session.add(model)
            PostgresUtils.db.session.commit()
            return UserMapper.to_helper(model)
        except IntegrityError:
            PostgresUtils.db.session.rollback()
            raise Exception(UserHelper.Errors.DUPLICATE_USERNAME)

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[UserHelper]:
        model = UserModel.query.filter_by(username=username).first()
        if model and model.check_password(password):
            return UserMapper.to_helper(model)
        return None

    @staticmethod
    def delete(user_id: int) -> None:
        user = UserModel.query.get(user_id)
        if user:
            PostgresUtils.db.session.delete(user)
            PostgresUtils.db.session.commit()
