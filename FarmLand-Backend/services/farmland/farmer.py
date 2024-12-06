from typing import List, Optional, Dict
from helpers.farmer import FarmerHelper
from helpers.schedule import ScheduleHelper
from repositories.farmer import FarmerRepository
from helpers.api_response import Error, ErrorAdditionalInfo
from repositories.schedule import ScheduleRepository
from repositories.farm import FarmRepository
from utils.helpers import calculate_fertilizer_cost

class FarmerService:
    @staticmethod
    def create_farmer(farmer: FarmerHelper) -> FarmerHelper:
        if not farmer.validate():
            raise Exception("Invalid farmer data")
        return FarmerRepository.create(farmer)

    @staticmethod
    def update_farmer(farmer: FarmerHelper) -> FarmerHelper:
        if not farmer.validate():
            raise Exception("Invalid farmer data")
        return FarmerRepository.update(farmer)

    @staticmethod
    def get_farmer_by_id(farmer_id: int) -> Optional[FarmerHelper]:
        farmer = FarmerRepository.get_by_id(farmer_id)
        if not farmer:
            raise Exception(FarmerHelper.Errors.FARMER_NOT_FOUND)
        return farmer

    @staticmethod
    def get_farmer_by_phone(phone_number: str) -> Optional[FarmerHelper]:
        return FarmerRepository.get_by_phone(phone_number)

    @staticmethod
    def get_all_farmers() -> List[FarmerHelper]:
        return FarmerRepository.get_all()

    @staticmethod
    def get_farmer_schedules(farmer_id: int) -> List[ScheduleHelper]:
        # Verify farmer exists
        farmer = FarmerRepository.get_by_id(farmer_id)
        if not farmer:
            raise Exception(FarmerHelper.Errors.FARMER_NOT_FOUND)
        return ScheduleRepository.get_farmer_schedules(farmer_id)

    @staticmethod
    def get_farmer_bill(farmer_id: int) -> Dict:
        # Verify farmer exists
        farmer = FarmerRepository.get_by_id(farmer_id)
        if not farmer:
            raise Exception(FarmerHelper.Errors.FARMER_NOT_FOUND)
        
        # Get all farm schedules for this farmer
        farm_schedules = ScheduleRepository.get_farm_schedules_with_farms(farmer_id)
        if not farm_schedules:
            return {
                'farmer_id': farmer_id,
                'farmer_name': farmer.name,
                'total_cost': 0,
                'farms': []
            }
        
        farms_bill = []
        total_cost = 0
        
        for farm, schedule in farm_schedules:
            cost = calculate_fertilizer_cost(
                schedule.fertilizer_type,
                schedule.quantity,
                farm.area
            )
            total_cost += cost
            farms_bill.append({
                'farm_id': farm.id,
                'village': farm.village,
                'crop': farm.crop_grown,
                'area': farm.area,
                'fertilizer_type': schedule.fertilizer_type,
                'quantity': schedule.quantity,
                'quantity_unit': schedule.quantity_unit,
                'cost': cost
            })
        
        return {
            'farmer_id': farmer_id,
            'farmer_name': farmer.name,
            'total_cost': total_cost,
            'farms': farms_bill
        }

    @staticmethod
    def get_farmers_by_crop(crop_type: str) -> List[FarmerHelper]:
        return FarmerRepository.get_farmers_by_crop(crop_type)
