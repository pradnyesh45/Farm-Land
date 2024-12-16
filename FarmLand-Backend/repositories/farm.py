from typing import Optional, List
from models.farm import FarmModel
from helpers.farm import FarmHelper
from mappers.farm import FarmMapper
from utils.postgres import PostgresUtils
from sqlalchemy.exc import IntegrityError

class FarmRepository:
    @staticmethod
    def get_by_id(farm_id: int) -> Optional[FarmHelper]:
        farm = FarmModel.query.get(farm_id)
        return FarmMapper.to_helper(farm) if farm else None

    @staticmethod
    def get_by_farmer_id(farmer_id: int) -> List[FarmHelper]:
        farms = FarmModel.query.filter_by(farmer_id=farmer_id)\
            .order_by(FarmModel.updated_at.desc()).all()
        return FarmMapper.to_helper_list(farms)

    @staticmethod
    def get_all() -> List[FarmHelper]:
        farms = FarmModel.query.order_by(FarmModel.updated_at.desc()).all()
        return FarmMapper.to_helper_list(farms)

    @staticmethod
    def create(helper: FarmHelper) -> FarmHelper:
        try:
            model = FarmMapper.to_model(helper)
            PostgresUtils.db.session.add(model)
            PostgresUtils.db.session.commit()
            return FarmMapper.to_helper(model)
        except IntegrityError:
            PostgresUtils.db.session.rollback()
            raise Exception("Failed to create farm")

    @staticmethod
    def update(helper: FarmHelper) -> FarmHelper:
        model = FarmModel.query.get(helper.id)
        if not model:
            raise Exception(FarmHelper.Errors.FARM_NOT_FOUND)
        
        model.village = helper.village
        model.area = helper.area
        model.crop_grown = helper.crop_grown
        
        try:
            PostgresUtils.db.session.commit()
            return FarmMapper.to_helper(model)
        except IntegrityError:
            PostgresUtils.db.session.rollback()
            raise Exception("Failed to update farm")
