from database import db
from database.models.farmer import FarmerDB
from database.models.farm import FarmDB
from database.models.schedule import ScheduleDB
from datetime import date, timedelta

def seed_database():
    if FarmerDB.query.first() is not None:
        print("Seed Database already exists")
        return

    # Clear existing data
    ScheduleDB.query.delete()
    FarmDB.query.delete()
    FarmerDB.query.delete()

    # Seed farmers
    farmers = [
        FarmerDB(phone_number="+91-9876543210", name="Pradnyesh Aglawe", language="Marathi"),
        FarmerDB(phone_number="+91-9876543211", name="Harsh Mehta", language="Gujrati"),
        FarmerDB(phone_number="+91-9876543212", name="Kapil Bhatia", language="Punjabi"),
        FarmerDB(phone_number="+91-9876543213", name="Venkatesh Banoth", language="Telugu"),
    ]
    db.session.add_all(farmers)
    db.session.commit()

    # Seed farms
    farms = [
        FarmDB(area=2.5, village="Paloti", crop_grown="Wheat", sowing_date=date.today() - timedelta(days=10), farmer_id=farmers[0].id),
        FarmDB(area=4.3, village="Rakdi", crop_grown="Rice", sowing_date=date.today() - timedelta(days=5), farmer_id=farmers[1].id),
        FarmDB(area=3.2, village="Satiala", crop_grown="Cotton", sowing_date=date.today() - timedelta(days=1), farmer_id=farmers[2].id),
        FarmDB(area=1.5, village="Ryakam", crop_grown="Soyabean", sowing_date=date.today(), farmer_id=farmers[3].id),
    ]
    db.session.add_all(farms)
    db.session.commit()

    # Seed schedules
    schedules = [
        # Schedule for Wheat
        ScheduleDB(days_after_sowing=10, fertilizer_type="Urea", quantity=100, quantity_unit="kg", farm_id=farms[0].id),
        ScheduleDB(days_after_sowing=15, fertilizer_type="DAP", quantity=50, quantity_unit="kg", farm_id=farms[0].id),
        # Schedule for Rice
        ScheduleDB(days_after_sowing=5, fertilizer_type="Urea", quantity=100, quantity_unit="kg", farm_id=farms[1].id),
        ScheduleDB(days_after_sowing=15, fertilizer_type="Micronutrient", quantity=50, quantity_unit="mL", farm_id=farms[1].id),
        # Schedule for Cotton
        ScheduleDB(days_after_sowing=10, fertilizer_type="Urea", quantity=100, quantity_unit="kg", farm_id=farms[2].id),
        ScheduleDB(days_after_sowing=15, fertilizer_type="NPK", quantity=50, quantity_unit="g", farm_id=farms[2].id),
        # Schedule for Soyabean
        ScheduleDB(days_after_sowing=10, fertilizer_type="NPK", quantity=100, quantity_unit="g", farm_id=farms[3].id),
        ScheduleDB(days_after_sowing=15, fertilizer_type="DAP", quantity=50, quantity_unit="kg", farm_id=farms[3].id),
    ]
    db.session.add_all(schedules)
    db.session.commit()

    print("Database seeded successfully")

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    seed_database()
    print("Seed Database created successfully")