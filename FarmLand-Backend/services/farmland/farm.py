from typing import List, Optional
from helpers.farm import FarmHelper
from repositories.farm import FarmRepository
from helpers.api_response import Error, ErrorAdditionalInfo

class FarmService:
    @staticmethod
    def create_farm(farm: FarmHelper) -> FarmHelper:
        if not farm.validate():
            raise Exception("Invalid farm data")
        return FarmRepository.create(farm)

    @staticmethod
    def update_farm(farm: FarmHelper) -> FarmHelper:
        if not farm.validate():
            raise Exception("Invalid farm data")
        return FarmRepository.update(farm)

    @staticmethod
    def get_farm_by_id(farm_id: int) -> Optional[FarmHelper]:
        farm = FarmRepository.get_by_id(farm_id)
        if not farm:
            raise Exception(FarmHelper.Errors.FARM_NOT_FOUND)
        return farm

    @staticmethod
    def get_farms_by_farmer(farmer_id: int) -> List[FarmHelper]:
        return FarmRepository.get_by_farmer_id(farmer_id)

    @staticmethod
    def get_all_farms() -> List[FarmHelper]:
        return FarmRepository.get_all()
