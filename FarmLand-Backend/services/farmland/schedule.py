from typing import List, Optional
from helpers.schedule import ScheduleHelper
from repositories.schedule import ScheduleRepository
from services.farmland.farm import FarmService
from helpers.api_response import Error, ErrorAdditionalInfo
from datetime import datetime, timedelta

class ScheduleService:
    @staticmethod
    def create_schedule(schedule: ScheduleHelper) -> ScheduleHelper:
        # Validate schedule data
        if not schedule.validate():
            raise Exception("Invalid schedule data")
        
        # Verify farm exists
        FarmService.get_farm_by_id(schedule.farm_id)
        
        return ScheduleRepository.create(schedule)

    @staticmethod
    def update_schedule(schedule: ScheduleHelper) -> ScheduleHelper:
        if not schedule.validate():
            raise Exception("Invalid schedule data")
        return ScheduleRepository.update(schedule)

    @staticmethod
    def get_schedule_by_id(schedule_id: int) -> Optional[ScheduleHelper]:
        schedule = ScheduleRepository.get_by_id(schedule_id)
        if not schedule:
            raise Exception(ScheduleHelper.Errors.SCHEDULE_NOT_FOUND)
        return schedule

    @staticmethod
    def get_schedules_by_farm(farm_id: int) -> List[ScheduleHelper]:
        # Verify farm exists
        FarmService.get_farm_by_id(farm_id)
        return ScheduleRepository.get_by_farm_id(farm_id)

    @staticmethod
    def get_all_schedules() -> List[ScheduleHelper]:
        return ScheduleRepository.get_all()

    @staticmethod
    def get_schedules_by_date_range(start_date: datetime, end_date: datetime) -> List[ScheduleHelper]:
        if start_date > end_date:
            raise Exception("Start date must be before end date")
        return ScheduleRepository.get_by_date_range(start_date, end_date)

    @staticmethod
    def get_farm_schedules_by_date_range(farm_id: int, start_date: datetime, end_date: datetime) -> List[ScheduleHelper]:
        if start_date > end_date:
            raise Exception("Start date must be before end date")
        # Verify farm exists
        FarmService.get_farm_by_id(farm_id)
        return ScheduleRepository.get_by_farm_and_date_range(farm_id, start_date, end_date)

    @staticmethod
    def get_due_schedules(days: int = 1) -> List[ScheduleHelper]:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=days)
        return ScheduleRepository.get_due_schedules(start_date, end_date)
