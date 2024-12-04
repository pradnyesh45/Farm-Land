from flask import Blueprint, jsonify, request
from services.farmer_service import FarmerService
from mappers.dto.farmer_dto import FarmerDTOMapper, FarmerCreateRequest, FarmerUpdateRequest

farmer_bp = Blueprint('farmer', __name__)
farmer_service = FarmerService()
dto_mapper = FarmerDTOMapper()

@farmer_bp.route('/farmers', methods=['GET'])
def get_all_farmers():
    farmers = farmer_service.get_all_farmers()
    return jsonify(dto_mapper.to_response_list(farmers))

@farmer_bp.route('/farmers/by-crop/<crop_name>', methods=['GET'])
def get_farmers_by_crop(crop_name):
    farmers = farmer_service.get_farmers_by_crop(crop_name)
    return jsonify(dto_mapper.to_response_list(farmers))

@farmer_bp.route('/farmers/<int:farmer_id>/bill', methods=['GET'])
def get_farmer_bill(farmer_id):
    try:
        bill = farmer_service.get_farmer_bill(farmer_id)
        return jsonify(bill)
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@farmer_bp.route('/farmers', methods=['POST'])
def add_farmer():
    try:
        request_data: FarmerCreateRequest = request.json
        farmer = dto_mapper.to_domain(request_data)
        created_farmer = farmer_service.create_farmer(farmer)
        return jsonify(dto_mapper.to_response(created_farmer)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@farmer_bp.route('/farmers/<int:farmer_id>', methods=['PUT'])
def update_farmer(farmer_id):
    try:
        request_data: FarmerUpdateRequest = request.json
        farmer = dto_mapper.to_domain(request_data)
        farmer.id = farmer_id
        updated_farmer = farmer_service.update_farmer(farmer)
        return jsonify(dto_mapper.to_response(updated_farmer))
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@farmer_bp.route('/farmers/<int:farmer_id>', methods=['DELETE'])
def delete_farmer(farmer_id):
    try:
        farmer_service.delete_farmer(farmer_id)
        return jsonify({'message': 'Farmer deleted successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404