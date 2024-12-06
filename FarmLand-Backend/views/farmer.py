from flask import Blueprint, request
from services.farmland.farmer import FarmerService
from helpers.farmer import FarmerHelper
from helpers.api_response import ApiResponse
from utils.api import ApiUtils
from middlewares.auth import authentication_middleware
from helpers.auth import AuthEntityType

farmer_view = Blueprint('farmer', __name__)

@farmer_view.route('/farmers', methods=['POST'])
@authentication_middleware(AuthEntityType.ADMIN)
def create_farmer():
    try:
        request_data = request.get_json()
        farmer = FarmerHelper(
            phone_number=request_data['phone_number'],
            name=request_data['name'],
            language=request_data['language']
        )
        created_farmer = FarmerService.create_farmer(farmer)
        
        api_response = ApiResponse(
            data={
                'id': created_farmer.id,
                'phone_number': created_farmer.phone_number,
                'name': created_farmer.name,
                'language': created_farmer.language
            },
            msg="Farmer created successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farmer_view.route('/farmers/<int:farmer_id>', methods=['PUT'])
@authentication_middleware(AuthEntityType.ADMIN)
def update_farmer(farmer_id):
    try:
        # Get existing farmer
        existing_farmer = FarmerService.get_farmer_by_id(farmer_id)
        request_data = request.get_json()
        
        # Update only provided fields
        farmer = FarmerHelper(
            id=farmer_id,
            phone_number=request_data.get('phone_number', existing_farmer.phone_number),
            name=request_data.get('name', existing_farmer.name),
            language=request_data.get('language', existing_farmer.language)
        )
        
        updated_farmer = FarmerService.update_farmer(farmer)
        
        api_response = ApiResponse(
            data={
                'id': updated_farmer.id,
                'phone_number': updated_farmer.phone_number,
                'name': updated_farmer.name,
                'language': updated_farmer.language
            },
            msg="Farmer updated successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farmer_view.route('/farmers/<int:farmer_id>', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_farmer(farmer_id):
    try:
        farmer = FarmerService.get_farmer_by_id(farmer_id)
        print(f"farmer: {farmer}")
        
        api_response = ApiResponse(
            data={
                'id': farmer.id,
                'phone_number': farmer.phone_number,
                'name': farmer.name,
                'language': farmer.language
            },
            msg="Farmer retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farmer_view.route('/farmers', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_all_farmers():
    try:
        farmers = FarmerService.get_all_farmers()
        farmer_list = [{
            'id': farmer.id,
            'phone_number': farmer.phone_number,
            'name': farmer.name,
            'language': farmer.language
        } for farmer in farmers]
        
        api_response = ApiResponse(
            data=farmer_list,
            msg="Farmers retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farmer_view.route('/farmers/<int:farmer_id>/bill', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_farmer_bill(farmer_id):
    try:
        bill = FarmerService.get_farmer_bill(farmer_id)
        
        api_response = ApiResponse(
            data=bill,
            msg="Farmer bill retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farmer_view.route('/farmers/by-crop/<string:crop_type>', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_farmers_by_crop(crop_type):
    try:
        if not crop_type:
            raise Exception("Crop type is required")
            
        farmers = FarmerService.get_farmers_by_crop(crop_type)
        farmer_list = [{
            'id': farmer.id,
            'name': farmer.name,
            'phone_number': farmer.phone_number,
            'language': farmer.language
        } for farmer in farmers]
        
        api_response = ApiResponse(
            data=farmer_list,
            msg=f"Farmers growing {crop_type} retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@farmer_view.route('/farmers/<int:farmer_id>', methods=['DELETE'])
@authentication_middleware(AuthEntityType.ADMIN)
def delete_farmer(farmer_id):
    try:
        FarmerService.delete_farmer(farmer_id)
        
        api_response = ApiResponse(
            data=None,
            msg=f"Farmer with ID {farmer_id} deleted successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)
