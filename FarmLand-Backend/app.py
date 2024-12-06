from flask import Flask
from flask_jwt_extended import JWTManager
from utils.postgres import PostgresUtils
from flask_migrate import Migrate
from views.user import user_view
from views.farmer import farmer_view
from views.farm import farm_view
from views.schedule import schedule_view
from sqlalchemy_utils import database_exists, create_database
from seed_data import seed_database
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password123@localhost:5432/farmer_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    jwt = JWTManager(app)

    # Initialize extensions
    PostgresUtils.db.init_app(app)
    Migrate(app, PostgresUtils.db)

    # Register blueprints
    app.register_blueprint(user_view, url_prefix='/api')
    app.register_blueprint(farmer_view, url_prefix='/api')
    app.register_blueprint(farm_view, url_prefix='/api')
    app.register_blueprint(schedule_view, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            print("Database created")
        PostgresUtils.db.create_all()
        seed_database()  # Ensure initial data is seeded
    app.run(host='0.0.0.0', debug=True)