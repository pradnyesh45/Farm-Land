from typing import List, Optional
from domain.models.farmer import Farmer
from database.models.farmer import FarmerDB
from database.models.farm import FarmDB
from database.models.schedule import ScheduleDB
from mappers.domain.farmer_mapper import FarmerDomainMapper
from database import db
from sqlalchemy import func

class FarmerRepository:
    def __init__(self):
        self.mapper = FarmerDomainMapper()
    
    def get_all(self) -> List[Farmer]:
        db_farmers = FarmerDB.query.all()
        return [self.mapper.to_domain(f) for f in db_farmers]
    
    def get_by_id(self, farmer_id: int) -> Optional[Farmer]:
        db_farmer = FarmerDB.query.get(farmer_id)
        return self.mapper.to_domain(db_farmer) if db_farmer else None
    
    def get_by_crop(self, crop_name: str) -> List[Farmer]:
        farmers = (db.session.query(FarmerDB)
                  .join(FarmDB, FarmerDB.id == FarmDB.farmer_id)
                  .filter(func.lower(FarmDB.crop_grown) == func.lower(crop_name))
                  .distinct()
                  .all())
        return [self.mapper.to_domain(f) for f in farmers]
    
    def create(self, farmer: Farmer) -> Farmer:
        db_farmer = self.mapper.to_db_model(farmer)
        db.session.add(db_farmer)
        db.session.commit()
        return self.mapper.to_domain(db_farmer)
    
    def update(self, farmer: Farmer) -> Optional[Farmer]:
        db_farmer = FarmerDB.query.get(farmer.id)
        if not db_farmer:
            return None
        
        db_farmer.name = farmer.name
        db_farmer.phone_number = farmer.phone_number
        db_farmer.language = farmer.language
        
        db.session.commit()
        return self.mapper.to_domain(db_farmer)
    
    def delete(self, farmer_id: int) -> bool:
        db_farmer = FarmerDB.query.get(farmer_id)
        if db_farmer:
            db.session.delete(db_farmer)
            db.session.commit()
            return True
        return False
    
    def get_farm_schedules(self, farmer_id: int) -> List[tuple]:
        return (db.session.query(FarmDB, ScheduleDB)
                .join(ScheduleDB, FarmDB.id == ScheduleDB.farm_id)
                .filter(FarmDB.farmer_id == farmer_id)
                .all())
        