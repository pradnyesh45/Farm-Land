from domain.models.farmer import Farmer
from database.models.farmer import FarmerDB

class FarmerDomainMapper:
    @staticmethod
    def to_domain(db_model: FarmerDB) -> Farmer:
        return Farmer(
            id=db_model.id,
            name=db_model.name,
            phone_number=db_model.phone_number,
            language=db_model.language
        )
    
    @staticmethod
    def to_db_model(domain: Farmer) -> FarmerDB:
        return FarmerDB(
            id=domain.id,
            name=domain.name,
            phone_number=domain.phone_number,
            language=domain.language
        )