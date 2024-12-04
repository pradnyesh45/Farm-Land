from flask import Blueprint, jsonify, request
from services.schedule_service import ScheduleService
from mappers.dto.schedule_dto import ScheduleDTOMapper, ScheduleCreateRequest, ScheduleUpdateRequest

schedule_bp = Blueprint('schedule', __name__)
schedule_service = ScheduleService()
dto_mapper = ScheduleDTOMapper()

@schedule_bp.route('/schedules', methods=['GET'])
def get_all_schedules():
    schedules = schedule_service.get_all_schedules()
    return jsonify(dto_mapper.to_response_list(schedules))

@schedule_bp.route('/schedules/due', methods=['GET'])
def get_due_schedules():
    schedules = schedule_service.get_due_schedules()
    return jsonify(schedules)

@schedule_bp.route('/schedules', methods=['POST'])
def add_schedule():
    try:
        request_data: ScheduleCreateRequest = request.json
        schedule = dto_mapper.to_domain(request_data)
        created_schedule = schedule_service.create_schedule(schedule)
        return jsonify(dto_mapper.to_response(created_schedule)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@schedule_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    try:
        request_data: ScheduleUpdateRequest = request.json
        schedule = dto_mapper.to_domain(request_data)
        updated_schedule = schedule_service.update_schedule(schedule_id, schedule)
        return jsonify(dto_mapper.to_response(updated_schedule))
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@schedule_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        schedule_service.delete_schedule(schedule_id)
        return jsonify({'message': 'Schedule deleted'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404