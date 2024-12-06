from helpers.user import UserHelper
from helpers.farmer import FarmerHelper
from helpers.farm import FarmHelper
from helpers.schedule import ScheduleHelper
from services.farmland.user import UserService
from services.farmland.farmer import FarmerService
from services.farmland.farm import FarmService
from services.farmland.schedule import ScheduleService
from datetime import datetime, timedelta

def seed_database():
    try:
        # Create initial users if they don't exist
        initial_users = [
            UserHelper(
                username='superadmin',
                password='superadmin123',
                role='SuperUser'
            ),
            UserHelper(
                username='admin1',
                password='admin1',
                role='Admin'
            ),
            UserHelper(
                username='user1',
                password='user1',
                role='User'
            )
        ]

        for user in initial_users:
            existing_user = UserService.get_user_by_username(user.username)
            if not existing_user:
                if user.role == 'SuperUser':
                    UserService.create_superuser(user)
                elif user.role == 'Admin':
                    UserService.create_admin(user)
                else:
                    UserService.create_user(user)
                print(f"{user.role} '{user.username}' created")
            else:
                print(f"{user.role} '{user.username}' already exists")


        # Seed farmers with their languages
        farmers = [
            FarmerHelper(
                phone_number="+91-9876543210",
                name="Pradnyesh Aglawe",
                language="Marathi"
            ),
            FarmerHelper(
                phone_number="+91-9876543211",
                name="Harsh Mehta",
                language="Gujarati"
            ),
            FarmerHelper(
                phone_number="+91-9876543212",
                name="Kapil Bhatia",
                language="Punjabi"
            ),
            FarmerHelper(
                phone_number="+91-9876543213",
                name="Venkatesh Banoth",
                language="Telugu"
            ),
        ]

        created_farmers = []
        for farmer in farmers:
            existing_farmer = FarmerService.get_farmer_by_phone(farmer.phone_number)
            if not existing_farmer:
                created_farmer = FarmerService.create_farmer(farmer)
                created_farmers.append(created_farmer)
                print(f"Farmer {farmer.name} created")
            else:
                print(f"Farmer with phone number {farmer.phone_number} already exists")
                created_farmers.append(existing_farmer)

        # Seed farms with sowing dates
        farms = [
            FarmHelper(
                farmer_id=created_farmers[0].id,
                area=10.5,
                village="Pune",
                crop_grown="Wheat",
                sowing_date=datetime.now() - timedelta(days=15)  # Sown 15 days ago
            ),
            FarmHelper(
                farmer_id=created_farmers[1].id,
                area=8.0,
                village="Ahmedabad",
                crop_grown="Rice",
                sowing_date=datetime.now() - timedelta(days=30)  # Sown 30 days ago
            ),
            FarmHelper(
                farmer_id=created_farmers[2].id,
                area=12.0,
                village="Amritsar",
                crop_grown="Corn",
                sowing_date=datetime.now() - timedelta(days=45)  # Sown 45 days ago
            ),
            FarmHelper(
                farmer_id=created_farmers[3].id,
                area=15.0,
                village="Hyderabad",
                crop_grown="Cotton",
                sowing_date=datetime.now()  # Sown today
            ),
        ]

        created_farms = []
        for farm in farms:
            # Check if farm exists for the farmer
            existing_farms = FarmService.get_farms_by_farmer(farm.farmer_id)
            farm_exists = any(
                existing_farm.village == farm.village and 
                existing_farm.crop_grown == farm.crop_grown 
                for existing_farm in existing_farms
            )
            
            if not farm_exists:
                created_farm = FarmService.create_farm(farm)
                created_farms.append(created_farm)
                print(f"Farm in {farm.village} created for crop {farm.crop_grown}")
            else:
                print(f"Farm already exists in {farm.village} for crop {farm.crop_grown}")
                # Use the existing farm for schedules
                created_farms.append(existing_farms[0])

        # Seed schedules with days after sowing and fertilizer details
        schedules = [
            # For Wheat (First Farm)
            ScheduleHelper(
                farm_id=created_farms[0].id,
                days_after_sowing=15,  # Due today
                fertilizer_type="DAP",
                quantity=50,
                quantity_unit="kg"
            ),
            ScheduleHelper(
                farm_id=created_farms[0].id,
                days_after_sowing=16,  # Due tomorrow
                fertilizer_type="Urea",
                quantity=25,
                quantity_unit="kg"
            ),
            # For Rice (Second Farm)
            ScheduleHelper(
                farm_id=created_farms[1].id,
                days_after_sowing=30,  # Due today
                fertilizer_type="NPK",
                quantity=30,
                quantity_unit="kg"
            ),
            ScheduleHelper(
                farm_id=created_farms[1].id,
                days_after_sowing=31,  # Due tomorrow
                fertilizer_type="Micronutrients",
                quantity=2,
                quantity_unit="L"
            ),
            # Future schedules
            ScheduleHelper(
                farm_id=created_farms[2].id,
                days_after_sowing=50,  # Due in 5 days
                fertilizer_type="Urea",
                quantity=40,
                quantity_unit="kg"
            ),
            ScheduleHelper(
                farm_id=created_farms[3].id,
                days_after_sowing=1,  # Due tomorrow
                fertilizer_type="DAP",
                quantity=60,
                quantity_unit="kg"
            ),
        ]

        for schedule in schedules:
            # Check if schedule exists for the farm
            existing_schedules = ScheduleService.get_schedules_by_farm(schedule.farm_id)
            schedule_exists = any(
                existing_schedule.days_after_sowing == schedule.days_after_sowing and
                existing_schedule.fertilizer_type == schedule.fertilizer_type
                for existing_schedule in existing_schedules
            )
            
            if not schedule_exists:
                ScheduleService.create_schedule(schedule)
                print(f"Schedule created for farm {schedule.farm_id} at day {schedule.days_after_sowing}")
            else:
                print(f"Schedule already exists for farm {schedule.farm_id} at day {schedule.days_after_sowing}")
        
        print("Database seeding completed successfully")
        
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        raise e

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_database()