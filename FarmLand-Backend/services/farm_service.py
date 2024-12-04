from typing import List
from domain.models.farm import Farm
from repositories.farm_repository import FarmRepository

class FarmService:
    def __init__(self):
        self.repository = FarmRepository()
    
    def get_all_farms(self) -> List[Farm]:
        return self.repository.get_all()
    
    def get_farm(self, farm_id: int) -> Farm:
        farm = self.repository.get_by_id(farm_id)
        if not farm:
            raise ValueError(f"Farm with id {farm_id} not found")
        return farm
    
    def create_farm(self, farm: Farm) -> Farm:
        return self.repository.create(farm)
    
    def update_farm(self, farm: Farm) -> Farm:
        updated_farm = self.repository.update(farm)
        if not updated_farm:
            raise ValueError(f"Farm with id {farm.id} not found")
        return updated_farm
    
    def delete_farm(self, farm_id: int) -> None:
        if not self.repository.delete(farm_id):
            raise ValueError(f"Farm with id {farm_id} not found")