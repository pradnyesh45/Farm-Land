from flask import Blueprint, jsonify, request
from services.farm_service import FarmService
from mappers.dto.farm_dto import FarmDTOMapper, FarmCreateRequest, FarmUpdateRequest

farm_bp = Blueprint('farm', __name__)
farm_service = FarmService()
dto_mapper = FarmDTOMapper()

@farm_bp.route('/farms', methods=['GET'])
def get_all_farms():
    farms = farm_service.get_all_farms()
    return jsonify(dto_mapper.to_response_list(farms))

@farm_bp.route('/farms/<int:farm_id>', methods=['GET'])
def get_farm(farm_id):
    try:
        farm = farm_service.get_farm(farm_id)
        return jsonify(dto_mapper.to_response(farm))
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@farm_bp.route('/farms', methods=['POST'])
def add_farm():
    try:
        request_data: FarmCreateRequest = request.json
        farm = dto_mapper.to_domain(request_data)
        created_farm = farm_service.create_farm(farm)
        return jsonify(dto_mapper.to_response(created_farm)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@farm_bp.route('/farms/<int:farm_id>', methods=['PUT'])
def update_farm(farm_id):
    try:
        request_data: FarmUpdateRequest = request.json
        farm = dto_mapper.to_domain(request_data)
        farm.id = farm_id
        updated_farm = farm_service.update_farm(farm)
        return jsonify(dto_mapper.to_response(updated_farm))
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@farm_bp.route('/farms/<int:farm_id>', methods=['DELETE'])
def delete_farm(farm_id):
    try:
        farm_service.delete_farm(farm_id)
        return jsonify({'message': 'Farm deleted successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404