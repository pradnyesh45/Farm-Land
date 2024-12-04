from typing import List, Dict
from domain.models.farmer import Farmer
from repositories.farmer_repository import FarmerRepository
from utils.helpers import calculate_fertilizer_cost

class FarmerService:
    def __init__(self):
        self.repository = FarmerRepository()

    def get_all_farmers(self) -> List[Farmer]:
        return self.repository.get_all()
    
    def get_farmers_by_crop(self, crop_name: str) -> List[Farmer]:
        return self.repository.get_by_crop(crop_name)
    
    def create_farmer(self, farmer: Farmer) -> Farmer:
        return self.repository.create(farmer)
    
    def update_farmer(self, farmer: Farmer) -> Farmer:
        updated_farmer = self.repository.update(farmer)
        if not updated_farmer:
            raise ValueError(f"Farmer with id {farmer.id} not found")
        return updated_farmer
    
    def delete_farmer(self, farmer_id: int) -> None:
        if not self.repository.delete(farmer_id):
            raise ValueError(f"Farmer with id {farmer_id} not found")
    
    def get_farmer(self, farmer_id: int) -> Farmer:
        farmer = self.repository.get_by_id(farmer_id)
        if not farmer:
            raise ValueError(f"Farmer with id {farmer_id} not found")
        return farmer
    
    def get_farmer_bill(self, farmer_id: int) -> Dict:
        # First check if farmer exists
        farmer = self.repository.get_by_id(farmer_id)
        if not farmer:
            raise ValueError(f"Farmer with id {farmer_id} not found")
        
        # Get all farm schedules for this farmer
        farm_schedules = self.repository.get_farm_schedules(farmer_id)
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