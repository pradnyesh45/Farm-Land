from typing import List, Optional
from domain.models.farm import Farm
from database.models.farm import FarmDB
from mappers.domain.farm_mapper import FarmDomainMapper
from database import db

class FarmRepository:
    def __init__(self):
        self.mapper = FarmDomainMapper()
    
    def get_all(self) -> List[Farm]:
        db_farms = FarmDB.query.all()
        return [self.mapper.to_domain(f) for f in db_farms]
    
    def get_by_id(self, farm_id: int) -> Optional[Farm]:
        db_farm = FarmDB.query.get(farm_id)
        return self.mapper.to_domain(db_farm) if db_farm else None
    
    def create(self, farm: Farm) -> Farm:
        db_farm = self.mapper.to_db_model(farm)
        db.session.add(db_farm)
        db.session.commit()
        return self.mapper.to_domain(db_farm)
    
    def update(self, farm: Farm) -> Optional[Farm]:
        db_farm = FarmDB.query.get(farm.id)
        if not db_farm:
            return None
            
        db_farm.area = farm.area
        db_farm.village = farm.village
        db_farm.crop_grown = farm.crop_grown
        db_farm.sowing_date = farm.sowing_date
        db_farm.farmer_id = farm.farmer_id
        
        db.session.commit()
        return self.mapper.to_domain(db_farm)
    
    def delete(self, farm_id: int) -> bool:
        db_farm = FarmDB.query.get(farm_id)
        if db_farm:
            db.session.delete(db_farm)
            db.session.commit()
            return True
        return False