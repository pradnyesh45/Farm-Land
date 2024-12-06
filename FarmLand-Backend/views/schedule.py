from flask import Blueprint, request
from services.farmland.schedule import ScheduleService
from helpers.schedule import ScheduleHelper
from helpers.api_response import ApiResponse
from utils.api import ApiUtils
from middlewares.auth import authentication_middleware
from helpers.auth import AuthEntityType
from datetime import datetime
from services.farmland.farmer import FarmerService

schedule_view = Blueprint('schedule', __name__)

@schedule_view.route('/schedules', methods=['POST'])
@authentication_middleware(AuthEntityType.ADMIN)
def create_schedule():
    try:
        request_data = request.get_json()
        schedule = ScheduleHelper(
            farm_id=request_data['farm_id'],
            days_after_sowing=request_data['days_after_sowing'],
            fertilizer_type=request_data['fertilizer_type'],
            quantity=request_data['quantity'],
            quantity_unit=request_data['quantity_unit']
        )
        created_schedule = ScheduleService.create_schedule(schedule)
        
        api_response = ApiResponse(
            data={
                'id': created_schedule.id,
                'farm_id': created_schedule.farm_id,
                'days_after_sowing': created_schedule.days_after_sowing,
                'fertilizer_type': created_schedule.fertilizer_type,
                'quantity': created_schedule.quantity,
                'quantity_unit': created_schedule.quantity_unit
            },
            msg="Schedule created successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@schedule_view.route('/schedules/<int:schedule_id>', methods=['PUT'])
@authentication_middleware(AuthEntityType.ADMIN)
def update_schedule(schedule_id):
    try:
        request_data = request.get_json()
        schedule = ScheduleHelper(
            id=schedule_id,
            farm_id=request_data['farm_id'],
            days_after_sowing=request_data['days_after_sowing'],
            fertilizer_type=request_data['fertilizer_type'],
            quantity=request_data['quantity'],
            quantity_unit=request_data['quantity_unit']
        )
        updated_schedule = ScheduleService.update_schedule(schedule)
        
        api_response = ApiResponse(
            data={
                'id': updated_schedule.id,
                'farm_id': updated_schedule.farm_id,
                'days_after_sowing': updated_schedule.days_after_sowing,
                'fertilizer_type': updated_schedule.fertilizer_type,
                'quantity': updated_schedule.quantity,
                'quantity_unit': updated_schedule.quantity_unit
            },
            msg="Schedule updated successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@schedule_view.route('/schedules/<int:schedule_id>', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_schedule(schedule_id):
    try:
        schedule = ScheduleService.get_schedule_by_id(schedule_id)
        
        api_response = ApiResponse(
            data={
                'id': schedule.id,
                'farm_id': schedule.farm_id,
                'days_after_sowing': schedule.days_after_sowing,
                'fertilizer_type': schedule.fertilizer_type,
                'quantity': schedule.quantity,
                'quantity_unit': schedule.quantity_unit
            },
            msg="Schedule retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@schedule_view.route('/farms/<int:farm_id>/schedules', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_farm_schedules(farm_id):
    try:
        schedules = ScheduleService.get_schedules_by_farm(farm_id)
        schedule_list = [{
            'id': schedule.id,
            'farm_id': schedule.farm_id,
            'days_after_sowing': schedule.days_after_sowing,
            'fertilizer_type': schedule.fertilizer_type,
            'quantity': schedule.quantity,
            'quantity_unit': schedule.quantity_unit
        } for schedule in schedules]
        
        api_response = ApiResponse(
            data=schedule_list,
            msg="Schedules retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@schedule_view.route('/schedules', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_all_schedules():
    try:
        schedules = ScheduleService.get_all_schedules()
        schedule_list = [{
            'id': schedule.id,
            'farm_id': schedule.farm_id,
            'days_after_sowing': schedule.days_after_sowing,
            'fertilizer_type': schedule.fertilizer_type,
            'quantity': schedule.quantity,
            'quantity_unit': schedule.quantity_unit
        } for schedule in schedules]
        
        api_response = ApiResponse(
            data=schedule_list,
            msg="Schedules retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@schedule_view.route('/schedules/search', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def search_schedules():
    try:
        start_date = datetime.fromisoformat(request.args.get('start_date'))
        end_date = datetime.fromisoformat(request.args.get('end_date'))
        farm_id = request.args.get('farm_id')
        
        if farm_id:
            schedules = ScheduleService.get_farm_schedules_by_date_range(
                int(farm_id), start_date, end_date
            )
        else:
            schedules = ScheduleService.get_schedules_by_date_range(start_date, end_date)
        
        schedule_list = [{
            'id': schedule.id,
            'farm_id': schedule.farm_id,
            'days_after_sowing': schedule.days_after_sowing,
            'fertilizer_type': schedule.fertilizer_type,
            'quantity': schedule.quantity,
            'quantity_unit': schedule.quantity_unit
        } for schedule in schedules]
        
        api_response = ApiResponse(
            data=schedule_list,
            msg="Schedules retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@schedule_view.route('/farmers/<int:farmer_id>/schedules/all', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_farmer_all_schedules(farmer_id):
    try:
        schedules = FarmerService.get_farmer_schedules(farmer_id)
        
        schedule_list = [{
            'id': schedule.id,
            'farm_id': schedule.farm_id,
            'days_after_sowing': schedule.days_after_sowing,
            'fertilizer_type': schedule.fertilizer_type,
            'quantity': schedule.quantity,
            'quantity_unit': schedule.quantity_unit
        } for schedule in schedules]
        
        api_response = ApiResponse(
            data=schedule_list,
            msg="Farmer schedules retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)

@schedule_view.route('/schedules/due', methods=['GET'])
@authentication_middleware(AuthEntityType.USER)
def get_due_schedules():
    try:
        # Get both today's and tomorrow's schedules
        due_schedules = ScheduleService.get_due_schedules(1)
        
        def format_schedule(schedule):
            return {
                'id': schedule.id,
                'farm_id': schedule.farm_id,
                'days_after_sowing': schedule.days_after_sowing,
                'fertilizer_type': schedule.fertilizer_type,
                'quantity': schedule.quantity,
                'quantity_unit': schedule.quantity_unit
            }
        
        schedule_data = {
            'today_tomorrow': [format_schedule(schedule) for schedule in due_schedules]
        }
        
        api_response = ApiResponse(
            data=schedule_data,
            msg="Due schedules for today and tomorrow retrieved successfully"
        )
        return ApiUtils.get_api_response(api_response)
    except Exception as error:
        return ApiUtils.get_error_response(error)
