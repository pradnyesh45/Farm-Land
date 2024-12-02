from models import db, Farmer, Farm, Schedule
from datetime import date, timedelta

def seed_database(app):
    with app.app_context():
        if Farmer.query.first() is not None:
            print("Seed Database already exists")
            return

        Schedule.query.delete()
        Farm.query.delete()
        Farmer.query.delete()

        farmers = [
            Farmer(phone_number="+91-9876543210", name="Pradnyesh Aglawe", language="Marathi"),
            Farmer(phone_number="+91-9876543211", name="Harsh Mehta", language="Gujrati"),
            Farmer(phone_number="+91-9876543212", name="Kapil Bhatia", language="Punjabi"),
            Farmer(phone_number="+91-9876543213", name="Venkatesh Banoth", language="Telugu"),
        ]
        db.session.add_all(farmers)
        db.session.commit()

        farms = [
            Farm(area=2.5, village="Paloti", crop_grown="Wheat", sowing_date=date.today() - timedelta(days=10), farmer_id=farmers[0].id),
            Farm(area=4.3, village="Rakdi", crop_grown="Rice", sowing_date=date.today() - timedelta(days=5), farmer_id=farmers[1].id),
            Farm(area=3.2, village="Satiala", crop_grown="Cotton", sowing_date=date.today() - timedelta(days=1), farmer_id=farmers[2].id),
            Farm(area=1.5, village="Ryakam", crop_grown="Soyabean", sowing_date=date.today(), farmer_id=farmers[3].id),
        ]
        db.session.add_all(farms)
        db.session.commit()

        schedules = [
            # Schedule for Wheat
            Schedule(days_after_sowing=10, fertilizer_type="Urea", quantity=100, quantity_unit="kg", farm_id=farms[0].id),
            Schedule(days_after_sowing=15, fertilizer_type="DAP", quantity=50, quantity_unit="kg", farm_id=farms[0].id),
            # Schedule for Rice
            Schedule(days_after_sowing=5, fertilizer_type="Urea", quantity=100, quantity_unit="kg", farm_id=farms[1].id),
            Schedule(days_after_sowing=15, fertilizer_type="Micronutrient", quantity=50, quantity_unit="mL", farm_id=farms[1].id),
            # Schedule for Cotton
            Schedule(days_after_sowing=10, fertilizer_type="Urea", quantity=100, quantity_unit="kg", farm_id=farms[2].id),
            Schedule(days_after_sowing=15, fertilizer_type="NPK", quantity=50, quantity_unit="g", farm_id=farms[2].id),
            # Schedule for Soyabean
            Schedule(days_after_sowing=10, fertilizer_type="NPK", quantity=100, quantity_unit="g", farm_id=farms[3].id),
            Schedule(days_after_sowing=15, fertilizer_type="DAP", quantity=50, quantity_unit="kg", farm_id=farms[3].id),
        ]
        db.session.add_all(schedules)
        db.session.commit()

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    seed_database(app)
    print("Seed Database created successfully")