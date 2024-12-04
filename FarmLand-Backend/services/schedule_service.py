from typing import List
from datetime import datetime, timedelta
from domain.models.schedule import Schedule
from repositories.schedule_repository import ScheduleRepository
from utils.helpers import fertiliser_price_map

class ScheduleService:
    def __init__(self):
        self.repository = ScheduleRepository()
    
    def get_all_schedules(self) -> List[Schedule]:
        return self.repository.get_all()
    
    def create_schedule(self, schedule: Schedule) -> Schedule:
        if schedule.fertilizer_type not in fertiliser_price_map:
            raise ValueError(f'Invalid fertilizer type. Available types are: {", ".join(fertiliser_price_map.keys())}')
        return self.repository.create(schedule)
    
    def get_schedule(self, schedule_id: int) -> Schedule:
        schedule = self.repository.get_by_id(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found")
        return schedule
    
    def update_schedule(self, schedule_id: int, schedule: Schedule) -> Schedule:
        schedule.id = schedule_id
        updated_schedule = self.repository.update(schedule)
        if not updated_schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found")
        return updated_schedule
    
    def delete_schedule(self, schedule_id: int) -> None:
        if not self.repository.delete(schedule_id):
            raise ValueError(f"Schedule with id {schedule_id} not found")
    
    def get_due_schedules(self) -> List[dict]:
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        schedules = self.repository.get_due_schedules(today, tomorrow)
        return [{
            'schedule_id': schedule.id,
            'farm_id': farm.id,
            'farmer_id': farmer.id,
            'farmer_name': farmer.name,
            'farm_village': farm.village,
            'farm_crop_grown': farm.crop_grown,
            'due_date': str(due_date_val)
        } for schedule, farm, farmer, due_date_val in schedules]