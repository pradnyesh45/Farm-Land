from models.farm import FarmModel
from helpers.farm import FarmHelper

class FarmMapper:
    @staticmethod
    def to_model(helper: FarmHelper) -> FarmModel:
        return FarmModel(
            id=helper.id,
            farmer_id=helper.farmer_id,
            area=helper.area,
            village=helper.village,
            crop_grown=helper.crop_grown,
            sowing_date=helper.sowing_date
        )

    @staticmethod
    def to_helper(model: FarmModel) -> FarmHelper:
        return FarmHelper(
            id=model.id,
            farmer_id=model.farmer_id,
            area=model.area,
            village=model.village,
            crop_grown=model.crop_grown,
            sowing_date=model.sowing_date,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_helper_list(models: list[FarmModel]) -> list[FarmHelper]:
        return [FarmMapper.to_helper(model) for model in models]
