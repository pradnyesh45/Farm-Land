from domain.models.schedule import Schedule
from database.models.schedule import ScheduleDB

class ScheduleDomainMapper:
    @staticmethod
    def to_domain(db_model: ScheduleDB) -> Schedule:
        return Schedule(
            id=db_model.id,
            days_after_sowing=db_model.days_after_sowing,
            fertilizer_type=db_model.fertilizer_type,
            quantity=db_model.quantity,
            quantity_unit=db_model.quantity_unit,
            farm_id=db_model.farm_id
        )
    
    @staticmethod
    def to_db_model(domain: Schedule) -> ScheduleDB:
        return ScheduleDB(
            id=domain.id,
            days_after_sowing=domain.days_after_sowing,
            fertilizer_type=domain.fertilizer_type,
            quantity=domain.quantity,
            quantity_unit=domain.quantity_unit,
            farm_id=domain.farm_id
        )
