from typing import Optional, List
from models.farmer import FarmerModel
from helpers.farmer import FarmerHelper
from mappers.farmer import FarmerMapper
from utils.postgres import PostgresUtils
from sqlalchemy.exc import IntegrityError
from models.farm import FarmModel
from sqlalchemy import func

class FarmerRepository:
    @staticmethod
    def get_by_id(farmer_id: int) -> Optional[FarmerHelper]:
        farmer = FarmerModel.query.get(farmer_id)
        return FarmerMapper.to_helper(farmer) if farmer else None

    @staticmethod
    def get_by_phone(phone_number: str) -> Optional[FarmerHelper]:
        farmer = FarmerModel.query.filter_by(phone_number=phone_number).first()
        return FarmerMapper.to_helper(farmer) if farmer else None

    @staticmethod
    def get_all() -> List[FarmerHelper]:
        farmers = FarmerModel.query.all()
        return FarmerMapper.to_helper_list(farmers)

    @staticmethod
    def create(helper: FarmerHelper) -> FarmerHelper:
        try:
            model = FarmerMapper.to_model(helper)
            PostgresUtils.db.session.add(model)
            PostgresUtils.db.session.commit()
            return FarmerMapper.to_helper(model)
        except IntegrityError:
            PostgresUtils.db.session.rollback()
            raise Exception(FarmerHelper.Errors.DUPLICATE_PHONE)

    @staticmethod
    def update(helper: FarmerHelper) -> FarmerHelper:
        model = FarmerModel.query.get(helper.id)
        if not model:
            raise Exception(FarmerHelper.Errors.FARMER_NOT_FOUND)
        
        model.phone_number = helper.phone_number
        model.name = helper.name
        model.language = helper.language
        
        try:
            PostgresUtils.db.session.commit()
            return FarmerMapper.to_helper(model)
        except IntegrityError:
            PostgresUtils.db.session.rollback()
            raise Exception(FarmerHelper.Errors.DUPLICATE_PHONE)

    @staticmethod
    def get_farmers_by_crop(crop_type: str) -> List[FarmerHelper]:
        # Join farmers with their farms and filter by crop type (case-insensitive)
        farmers = PostgresUtils.db.session.query(FarmerModel).join(
            FarmModel, FarmerModel.id == FarmModel.farmer_id
        ).filter(
            func.lower(FarmModel.crop_grown) == func.lower(crop_type)
        ).distinct().all()
        
        return FarmerMapper.to_helper_list(farmers)

    @staticmethod
    def delete(farmer_id: int) -> None:
        farmer = FarmerModel.query.get(farmer_id)
        if farmer:
            PostgresUtils.db.session.delete(farmer)
            PostgresUtils.db.session.commit()
