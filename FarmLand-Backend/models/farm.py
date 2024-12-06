from utils.postgres import PostgresUtils
from datetime import datetime

class FarmModel(PostgresUtils.db.Model):
    __tablename__ = "farms"

    id = PostgresUtils.db.Column(PostgresUtils.db.Integer, primary_key=True)
    farmer_id = PostgresUtils.db.Column(PostgresUtils.db.Integer, PostgresUtils.db.ForeignKey('farmers.id'), nullable=False)
    area = PostgresUtils.db.Column(PostgresUtils.db.Float, nullable=False)
    village = PostgresUtils.db.Column(PostgresUtils.db.String(100), nullable=False)
    crop_grown = PostgresUtils.db.Column(PostgresUtils.db.String(100), nullable=False)
    sowing_date = PostgresUtils.db.Column(PostgresUtils.db.DateTime, nullable=False)
    created_at = PostgresUtils.db.Column(PostgresUtils.db.DateTime, default=datetime.utcnow)
    updated_at = PostgresUtils.db.Column(PostgresUtils.db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farmer = PostgresUtils.db.relationship('FarmerModel', backref='farms')
    schedules = PostgresUtils.db.relationship('ScheduleModel', back_populates='farm', lazy=True)

    def __init__(self, farmer_id: int, area: float, village: str, crop_grown: str, sowing_date: datetime, id: int = None):
        self.id = id
        self.farmer_id = farmer_id
        self.area = area
        self.village = village
        self.crop_grown = crop_grown
        self.sowing_date = sowing_date
