from typing import Optional, List
from models.schedule import ScheduleModel
from helpers.schedule import ScheduleHelper
from mappers.schedule import ScheduleMapper
from utils.postgres import PostgresUtils
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from models.farm import FarmModel
from sqlalchemy import func

class ScheduleRepository:
    @staticmethod
    def get_by_id(schedule_id: int) -> Optional[ScheduleHelper]:
        schedule = ScheduleModel.query.get(schedule_id)
        return ScheduleMapper.to_helper(schedule) if schedule else None

    @staticmethod
    def get_by_farm_id(farm_id: int) -> List[ScheduleHelper]:
        schedules = ScheduleModel.query.filter_by(farm_id=farm_id).all()
        return ScheduleMapper.to_helper_list(schedules)

    @staticmethod
    def get_all() -> List[ScheduleHelper]:
        schedules = ScheduleModel.query.all()
        return ScheduleMapper.to_helper_list(schedules)

    @staticmethod
    def create(helper: ScheduleHelper) -> ScheduleHelper:
        try:
            model = ScheduleMapper.to_model(helper)
            PostgresUtils.db.session.add(model)
            PostgresUtils.db.session.commit()
            return ScheduleMapper.to_helper(model)
        except IntegrityError:
            PostgresUtils.db.session.rollback()
            raise Exception("Failed to create schedule")

    @staticmethod
    def update(helper: ScheduleHelper) -> ScheduleHelper:
        model = ScheduleModel.query.get(helper.id)
        if not model:
            raise Exception(ScheduleHelper.Errors.SCHEDULE_NOT_FOUND)
        
        model.task = helper.task
        model.scheduled_date = helper.scheduled_date
        model.status = helper.status
        
        try:
            PostgresUtils.db.session.commit()
            return ScheduleMapper.to_helper(model)
        except IntegrityError:
            PostgresUtils.db.session.rollback()
            raise Exception("Failed to update schedule")

    @staticmethod
    def get_by_date_range(start_date: datetime, end_date: datetime) -> List[ScheduleHelper]:
        schedules = ScheduleModel.query.filter(
            ScheduleModel.scheduled_date.between(start_date, end_date)
        ).order_by(ScheduleModel.scheduled_date).all()
        return ScheduleMapper.to_helper_list(schedules)

    @staticmethod
    def get_by_farm_and_date_range(farm_id: int, start_date: datetime, end_date: datetime) -> List[ScheduleHelper]:
        schedules = ScheduleModel.query.filter(
            ScheduleModel.farm_id == farm_id,
            ScheduleModel.scheduled_date.between(start_date, end_date)
        ).order_by(ScheduleModel.scheduled_date).all()
        return ScheduleMapper.to_helper_list(schedules)

    @staticmethod
    def get_due_schedules(start_date: datetime, end_date: datetime) -> List[ScheduleHelper]:
        # Calculate due date using SQLAlchemy func to handle date arithmetic
        due_date = (func.date(FarmModel.sowing_date) + 
                    func.make_interval(0, 0, 0, ScheduleModel.days_after_sowing, 0, 0, 0)
                   ).label('due_date')
        
        schedules = PostgresUtils.db.session.query(ScheduleModel).join(
            FarmModel, ScheduleModel.farm_id == FarmModel.id
        ).filter(
            due_date.between(start_date, end_date)
        ).order_by(due_date).all()
        
        return ScheduleMapper.to_helper_list(schedules)

    @staticmethod
    def get_farmer_schedules(farmer_id: int) -> List[ScheduleHelper]:
        schedules = ScheduleModel.query.join(
            FarmModel, ScheduleModel.farm_id == FarmModel.id
        ).filter(
            FarmModel.farmer_id == farmer_id
        ).order_by(ScheduleModel.scheduled_date).all()
        return ScheduleMapper.to_helper_list(schedules)

    @staticmethod
    def get_farm_schedules_with_farms(farmer_id: int) -> List[tuple]:
        # Join schedules with farms and filter by farmer_id
        farm_schedules = PostgresUtils.db.session.query(
            FarmModel, ScheduleModel
        ).join(
            ScheduleModel, FarmModel.id == ScheduleModel.farm_id
        ).filter(
            FarmModel.farmer_id == farmer_id
        ).all()
        
        return farm_schedules
