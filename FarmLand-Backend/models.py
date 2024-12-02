from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
db = SQLAlchemy()

class Farmer(db.Model):
    __tablename__ = "farmers"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    farms = db.relationship("Farm", back_populates="farmer")

    def __repr__(self):
        return f"<Farmer {self.name}>"

class Farm(db.Model):
    __tablename__ = "farms"
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float, nullable=False)
    village = db.Column(db.String(100), nullable=False)
    crop_grown = db.Column(db.String(100), nullable=False)
    sowing_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id"), nullable=False)

    farmer = db.relationship("Farmer", back_populates="farms")
    schedules = db.relationship("Schedule", back_populates="farm")

class Schedule(db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    days_after_sowing = db.Column(db.Integer, nullable=False)
    fertilizer_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    quantity_unit = db.Column(Enum('ton', 'kg', 'g', 'L', 'mL', name='quantity_unit_enum'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id"), nullable=False)

    farm = db.relationship("Farm", back_populates="schedules")
