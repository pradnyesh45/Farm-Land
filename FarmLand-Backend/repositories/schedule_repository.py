from typing import List, Optional
from datetime import date
from domain.models.schedule import Schedule
from database.models.schedule import ScheduleDB
from database.models.farm import FarmDB
from database.models.farmer import FarmerDB
from mappers.domain.schedule_mapper import ScheduleDomainMapper
from database import db
from sqlalchemy import func

class ScheduleRepository:
    def __init__(self):
        self.mapper = ScheduleDomainMapper()
    
    def get_all(self) -> List[Schedule]:
        db_schedules = ScheduleDB.query.all()
        return [self.mapper.to_domain(s) for s in db_schedules]
    
    def get_by_id(self, schedule_id: int) -> Optional[Schedule]:
        db_schedule = ScheduleDB.query.get(schedule_id)
        return self.mapper.to_domain(db_schedule) if db_schedule else None
    
    def create(self, schedule: Schedule) -> Schedule:
        db_schedule = self.mapper.to_db_model(schedule)
        db.session.add(db_schedule)
        db.session.commit()
        return self.mapper.to_domain(db_schedule)
    
    def update(self, schedule: Schedule) -> Optional[Schedule]:
        db_schedule = ScheduleDB.query.get(schedule.id)
        if not db_schedule:
            return None
            
        db_schedule.days_after_sowing = schedule.days_after_sowing
        db_schedule.fertilizer_type = schedule.fertilizer_type
        db_schedule.quantity = schedule.quantity
        db_schedule.quantity_unit = schedule.quantity_unit
        db_schedule.farm_id = schedule.farm_id
        
        db.session.commit()
        return self.mapper.to_domain(db_schedule)
    
    def delete(self, schedule_id: int) -> bool:
        db_schedule = ScheduleDB.query.get(schedule_id)
        if db_schedule:
            db.session.delete(db_schedule)
            db.session.commit()
            return True
        return False
    
    def get_due_schedules(self, start_date: date, end_date: date) -> List[tuple]:
        due_date = (func.date(FarmDB.sowing_date) + 
                   func.make_interval(0, 0, 0, ScheduleDB.days_after_sowing, 0, 0, 0)
                   ).label('due_date')
        
        return (db.session.query(ScheduleDB, FarmDB, FarmerDB, due_date)
                .join(FarmDB, ScheduleDB.farm_id == FarmDB.id)
                .join(FarmerDB, FarmDB.farmer_id == FarmerDB.id)
                .filter(due_date.between(start_date, end_date))
                .all())