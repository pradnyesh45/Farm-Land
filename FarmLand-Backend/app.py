from flask import Flask
from database import db
from flask_migrate import Migrate
from api.routes.farmer_routes import farmer_bp
from api.routes.farm_routes import farm_bp
from api.routes.schedule_routes import schedule_bp
from seed_data import seed_database
from sqlalchemy_utils import database_exists, create_database
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password123@localhost:5432/farmer_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(farmer_bp, url_prefix='/api')
    app.register_blueprint(farm_bp, url_prefix='/api')
    app.register_blueprint(schedule_bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(app.config['SQLALCHEMY_DATABASE_URI'])
            print("Database created")
        db.create_all()
        seed_database()
    app.run(host='0.0.0.0', debug=True)