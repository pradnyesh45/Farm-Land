from domain.models.farm import Farm
from database.models.farm import FarmDB

class FarmDomainMapper:
    @staticmethod
    def to_domain(db_model: FarmDB) -> Farm:
        return Farm(
            id=db_model.id,
            area=db_model.area,
            village=db_model.village,
            crop_grown=db_model.crop_grown,
            sowing_date=db_model.sowing_date,
            farmer_id=db_model.farmer_id
        )
    
    @staticmethod
    def to_db_model(domain: Farm) -> FarmDB:
        return FarmDB(
            id=domain.id,
            area=domain.area,
            village=domain.village,
            crop_grown=domain.crop_grown,
            sowing_date=domain.sowing_date,
            farmer_id=domain.farmer_id
        )
