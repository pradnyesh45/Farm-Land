from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from models import db, Schedule, Farm, Farmer
from sqlalchemy import func
from utils import fertiliser_price_map
from werkzeug.exceptions import NotFound


api_bp = Blueprint('api', __name__)

# Find all schedules due for today/tomorrow
@api_bp.route('/schedules/due', methods=['GET'])
def get_due_schedules():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Calculate due_date using proper SQLAlchemy syntax
    due_date = (func.date(Farm.sowing_date) + 
                func.make_interval(0, 0, 0, Schedule.days_after_sowing, 0, 0, 0)
                ).label('due_date')
    
    due_schedules = (
        db.session.query(Schedule, Farm, Farmer, due_date)
        .join(Farm, Schedule.farm_id == Farm.id)
        .join(Farmer, Farm.farmer_id == Farmer.id)
        .filter(
            due_date.between(today, tomorrow)
        )
        .all()
    )

    result = [{
        'schedule_id': schedule.id,
        'farm_id': farm.id,
        'farmer_id': farmer.id,
        'farmer_name': farmer.name,
        'farm_village': farm.village,
        'farm_crop_grown': farm.crop_grown,
        'due_date': str(due_date_val)
    } for schedule, farm, farmer, due_date_val in due_schedules]
    
    return jsonify(result)

# Find all farmers who are growing a crop
@api_bp.route('/farmers/by-crop/<crop_name>', methods=['GET'])
def get_farmers_by_crop(crop_name):
    farmers = (
        db.session.query(Farmer)
        .join(Farm, Farmer.id == Farm.farmer_id)
        .filter(func.lower(Farm.crop_grown) == func.lower(crop_name))
        .distinct()
        .all()
    )
    result = [{'farmer_id': farmer.id, 
               'farmer_name': farmer.name
               }  for farmer in farmers]
    return jsonify(result)

# Given prices of fertilizers, calculate the bill of materials for a single farmer
@api_bp.route('/farmers/<farmer_id>/bill', methods=['GET'])
def get_farmer_bill(farmer_id):
    farm_schedules = (
        db.session.query(Farm, Schedule)
        .join(Schedule, Farm.id == Schedule.farm_id)
        .filter(Farm.farmer_id == farmer_id)
        .all()
    )
    if not farm_schedules: 
        return jsonify({
            'error': 'No farms or schedules found for this farmer' 
        }, 404)
    
    farms_bill = []
    for farm, schedule in farm_schedules:
        cost = (fertiliser_price_map.get(schedule.fertilizer_type, 0) * schedule.quantity * farm.area)
        farms_bill.append({
           'farm_id': farm.id,
           'village': farm.village,
           'crop': farm.crop_grown,
           'fertilizer_type': schedule.fertilizer_type,
           'cost': cost
        })
        result = {
            'farmer_id': farmer_id,
            'farms': farms_bill
        }
    return jsonify(result)

# Farmer Endpoints
@api_bp.route('/farmers', methods=['GET'])
def get_all_farmers():
    farmers = Farmer.query.all()
    result =[{
        'id': farmer.id,
        'name': farmer.name,
        'phone_number': farmer.phone_number,
        'language': farmer.language
    } for farmer in farmers]
    return jsonify(result)

@api_bp.route('/farmers', methods=['POST'])
def add_farmer():
    data = request.json

    #Validations
    required_fields = ['name', 'phone_number', 'language']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_farmer = Farmer(
        name=data['name'], 
        phone_number=data['phone_number'], 
        language=data['language']
        )
    db.session.add(new_farmer)
    db.session.commit()
    return jsonify({'id': new_farmer.id}), 201

@api_bp.route('/farmers/<int:farmer_id>', methods=['PUT'])
def update_farmer(farmer_id):
    data = request.json
    farmer = Farmer.query.get_or_404(farmer_id)
    farmer.name = data.get('name', farmer.name)
    farmer.phone_number = data.get('phone_number', farmer.phone_number)
    farmer.language = data.get('language', farmer.language)
    db.session.commit()
    return jsonify({'message': 'Farmer updated'})

@api_bp.route('/farmers/<int:farmer_id>', methods=['DELETE'])
def delete_farmer(farmer_id):
    farmer = Farmer.query.get_or_404(farmer_id)
    db.session.delete(farmer)
    db.session.commit()
    return jsonify({'message': 'Farmer deleted'})

# Farm Endpoints
@api_bp.route('/farms', methods=['GET'])
def get_all_farms():
    farms = Farm.query.all()
    result = [{
        'id': farm.id,
        'area': farm.area,
        'village': farm.village,
        'crop_grown': farm.crop_grown,
        'sowing_date': str(farm.sowing_date),
        'farmer_id': farm.farmer_id
    } for farm in farms]
    return jsonify(result)

@api_bp.route('/farms', methods=['POST'])
def add_farm():
    data = request.json

    #Validations
    required_fields = ['area', 'village', 'crop_grown', 'sowing_date', 'farmer_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        sowing_date = datetime.strptime(data['sowing_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    if not Farmer.query.get(data['farmer_id']):
        return jsonify({'error': 'Farmer not found'}), 404

    new_farm = Farm(
        area=data['area'], 
        village=data['village'], 
        crop_grown=data['crop_grown'], 
        sowing_date=sowing_date, 
        farmer_id=data['farmer_id']
        )
    db.session.add(new_farm)
    db.session.commit()
    return jsonify({'id': new_farm.id}), 201

@api_bp.route('/farms/<int:farm_id>', methods=['PUT'])
def update_farm(farm_id):
    data = request.json
    farm = Farm.query.get_or_404(farm_id)
    farm.area = data.get('area', farm.area)
    farm.village = data.get('village', farm.village)
    farm.crop_grown = data.get('crop_grown', farm.crop_grown)
    if 'sowing_date' in data:
        try:
            sowing_date = datetime.strptime(data['sowing_date'], '%Y-%m-%d')
            farm.sowing_date = sowing_date
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    db.session.commit()
    return jsonify({'message': 'Farm updated'})

@api_bp.route('/farms/<int:farm_id>', methods=['DELETE'])
def delete_farm(farm_id):
    farm = Farm.query.get_or_404(farm_id)
    db.session.delete(farm)
    db.session.commit()
    return jsonify({'message': 'Farm deleted'})

# Schedule Endpoints
@api_bp.route('/schedules', methods=['GET'])
def get_all_schedules():
    schedules = Schedule.query.all()
    result = [{
        'id': schedule.id,
        'days_after_sowing': schedule.days_after_sowing,
        'fertilizer_type': schedule.fertilizer_type,
        'quantity': schedule.quantity,
        'quantity_unit': schedule.quantity_unit,
        'farm_id': schedule.farm_id
    } for schedule in schedules]
    return jsonify(result)

@api_bp.route('/schedules', methods=['POST'])
def add_schedule():
    data = request.json

    #Validations
    required_fields = ['days_after_sowing', 'fertilizer_type', 'quantity', 'quantity_unit', 'farm_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    #Validation for fertilizer type
    if data['fertilizer_type'] not in fertiliser_price_map:
        return jsonify({'error': 'Invalid fertilizer type, Available types are: ' + ', '.join(fertiliser_price_map.keys())}), 400
    
    new_schedule = Schedule(
        days_after_sowing=data['days_after_sowing'], 
        fertilizer_type=data['fertilizer_type'], 
        quantity=data['quantity'], 
        quantity_unit=data['quantity_unit'], 
        farm_id=data['farm_id']
        )
    db.session.add(new_schedule)
    db.session.commit()
    return jsonify({'id': new_schedule.id}), 201

@api_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    data = request.json
    schedule = Schedule.query.get_or_404(schedule_id)
    schedule.days_after_sowing = data.get('days_after_sowing', schedule.days_after_sowing)
    schedule.fertilizer_type = data.get('fertilizer_type', schedule.fertilizer_type)
    schedule.quantity = data.get('quantity', schedule.quantity)
    schedule.quantity_unit = data.get('quantity_unit', schedule.quantity_unit)
    schedule.farm_id = data.get('farm_id', schedule.farm_id)
    db.session.commit()
    return jsonify({'message': 'Schedule updated'})

@api_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule deleted'})