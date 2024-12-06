from models.user import UserModel
from helpers.user import UserHelper

class UserMapper:
    @staticmethod
    def to_model(helper: UserHelper) -> UserModel:
        return UserModel(
            username=helper.username,
            role=helper.role,
            password=helper.password,
            id=helper.id
        )

    @staticmethod
    def to_helper(model: UserModel) -> UserHelper:
        return UserHelper(
            id=model.id,
            username=model.username,
            role=model.role,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_helper_list(models: list[UserModel]) -> list[UserHelper]:
        return [UserMapper.to_helper(model) for model in models]
