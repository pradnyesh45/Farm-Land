from database import db

class FarmerDB(db.Model):
    __tablename__ = 'farmers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    language = db.Column(db.String(20), nullable=False)
    
    farms = db.relationship('FarmDB', backref='farmer', lazy=True)
