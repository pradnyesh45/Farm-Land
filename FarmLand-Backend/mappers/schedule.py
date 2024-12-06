from models.schedule import ScheduleModel
from helpers.schedule import ScheduleHelper

class ScheduleMapper:
    @staticmethod
    def to_model(helper: ScheduleHelper) -> ScheduleModel:
        return ScheduleModel(
            id=helper.id,
            farm_id=helper.farm_id,
            days_after_sowing=helper.days_after_sowing,
            fertilizer_type=helper.fertilizer_type,
            quantity=helper.quantity,
            quantity_unit=helper.quantity_unit
        )

    @staticmethod
    def to_helper(model: ScheduleModel) -> ScheduleHelper:
        return ScheduleHelper(
            id=model.id,
            farm_id=model.farm_id,
            days_after_sowing=model.days_after_sowing,
            fertilizer_type=model.fertilizer_type,
            quantity=model.quantity,
            quantity_unit=model.quantity_unit,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_helper_list(models: list[ScheduleModel]) -> list[ScheduleHelper]:
        return [ScheduleMapper.to_helper(model) for model in models]
