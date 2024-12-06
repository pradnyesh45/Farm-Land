from models.farmer import FarmerModel
from helpers.farmer import FarmerHelper

class FarmerMapper:
    @staticmethod
    def to_model(helper: FarmerHelper) -> FarmerModel:
        return FarmerModel(
            id=helper.id,
            phone_number=helper.phone_number,
            name=helper.name,
            language=helper.language
        )

    @staticmethod
    def to_helper(model: FarmerModel) -> FarmerHelper:
        return FarmerHelper(
            id=model.id,
            phone_number=model.phone_number,
            name=model.name,
            language=model.language,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_helper_list(models: list[FarmerModel]) -> list[FarmerHelper]:
        return [FarmerMapper.to_helper(model) for model in models]
