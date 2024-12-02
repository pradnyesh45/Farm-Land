from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from models import db, Schedule, Farm, Farmer
from sqlalchemy import func
from utils import fertiliser_price_map
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
