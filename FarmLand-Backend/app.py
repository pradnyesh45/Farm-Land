from flask import Flask
from models import db
from flask_migrate import Migrate
from routes import api_bp
from seed_data import seed_database
from sqlalchemy_utils import database_exists, create_database
import os


def create_app():
    app = Flask(__name__)

    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password123@localhost:5432/farmer_db'
    ) 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        print("Database farmer_db created")
    
    #initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    #initialize seed data
    with app.app_context():
        db.create_all()
        seed_database(app)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)