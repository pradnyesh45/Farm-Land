from database import db
from datetime import date

class FarmDB(db.Model):
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float, nullable=False)
    village = db.Column(db.String(100), nullable=False)
    crop_grown = db.Column(db.String(50), nullable=False)
    sowing_date = db.Column(db.Date, nullable=False)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    
    schedules = db.relationship('ScheduleDB', backref='farm', lazy=True)
