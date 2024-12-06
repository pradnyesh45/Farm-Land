from utils.postgres import PostgresUtils
from datetime import datetime

class ScheduleModel(PostgresUtils.db.Model):
    __tablename__ = "schedules"

    id = PostgresUtils.db.Column(PostgresUtils.db.Integer, primary_key=True)
    farm_id = PostgresUtils.db.Column(PostgresUtils.db.Integer, PostgresUtils.db.ForeignKey('farms.id'), nullable=False)
    days_after_sowing = PostgresUtils.db.Column(PostgresUtils.db.Integer, nullable=False)
    fertilizer_type = PostgresUtils.db.Column(PostgresUtils.db.String(100), nullable=False)
    quantity = PostgresUtils.db.Column(PostgresUtils.db.Float, nullable=False)
    quantity_unit = PostgresUtils.db.Column(PostgresUtils.db.String(10), nullable=False)
    created_at = PostgresUtils.db.Column(PostgresUtils.db.DateTime, default=datetime.utcnow)
    updated_at = PostgresUtils.db.Column(PostgresUtils.db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    farm = PostgresUtils.db.relationship('FarmModel', back_populates='schedules')

    def __init__(self, farm_id: int, days_after_sowing: int, fertilizer_type: str, quantity: float, quantity_unit: str, id: int = None):
        self.id = id
        self.farm_id = farm_id
        self.days_after_sowing = days_after_sowing
        self.fertilizer_type = fertilizer_type
        self.quantity = quantity
        self.quantity_unit = quantity_unit
