from flask import Blueprint, request
from services.farmland.farm import FarmService
from helpers.farm import FarmHelper
from helpers.api_response import ApiResponse
from utils.api import ApiUtils
from middlewares.auth import authentication_middleware
from helpers.auth import AuthEntityType

farm_view = Blueprint('farm', __name__)

@farm_view.route('/farms', methods=['POST'])
@authentication_middleware(AuthEntityType.ADMIN)
def create_farm():
    try:
        request_data = request.get_json()
        farm = FarmHelper(
            farmer_id=request_data['farmer_id'],
            village=request_data['village'],
            area=float(request_data['area']),
            crop_grown=request_data['crop_grown']
        )
        created_farm = FarmService.create_farm(farm)
        
        api_response = ApiResponse(
            data={
                'id': created_farm.id,
                'farmer_id': created_farm.farmer_id,
                'village': created_farm.village,
                'area': created_farm.area,
                'crop_grown': created_farm.crop_grown
            },
            msg="Farm created successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farm_view.route('/farms/<int:farm_id>', methods=['PUT'])
@authentication_middleware(AuthEntityType.ADMIN)
def update_farm(farm_id):
    try:
        request_data = request.get_json()
        farm = FarmHelper(
            id=farm_id,
            farmer_id=request_data['farmer_id'],
            village=request_data['village'],
            area=float(request_data['area']),
            crop_grown=request_data['crop_grown']
        )
        updated_farm = FarmService.update_farm(farm)
        
        api_response = ApiResponse(
            data={
                'id': updated_farm.id,
                'farmer_id': updated_farm.farmer_id,
                'village': updated_farm.village,
                'area': updated_farm.area,
                'crop_grown': updated_farm.crop_grown
            },
            msg="Farm updated successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farm_view.route('/farms/<int:farm_id>', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_farm(farm_id):
    try:
        farm = FarmService.get_farm_by_id(farm_id)
        
        api_response = ApiResponse(
            data={
                'id': farm.id,
                'farmer_id': farm.farmer_id,
                'village': farm.village,
                'area': farm.area,
                'crop_grown': farm.crop_grown
            },
            msg="Farm retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farm_view.route('/farmers/<int:farmer_id>/farms', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_farmer_farms(farmer_id):
    try:
        farms = FarmService.get_farms_by_farmer(farmer_id)
        farm_list = [{
            'id': farm.id,
            'farmer_id': farm.farmer_id,
            'village': farm.village,
            'area': farm.area,
            'crop_grown': farm.crop_grown
        } for farm in farms]
        
        api_response = ApiResponse(
            data=farm_list,
            msg="Farms retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farm_view.route('/farms', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_all_farms():
    try:
        farms = FarmService.get_all_farms()
        farm_list = [{
            'id': farm.id,
            'farmer_id': farm.farmer_id,
            'village': farm.village,
            'area': farm.area,
            'crop_grown': farm.crop_grown
        } for farm in farms]
        
        api_response = ApiResponse(
            data=farm_list,
            msg="Farms retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)
