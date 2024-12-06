from utils.postgres import PostgresUtils
from utils.misc import MiscUtils
from datetime import datetime

class FarmerModel(PostgresUtils.db.Model):
    __tablename__ = "farmers"

    id = PostgresUtils.db.Column(PostgresUtils.db.Integer, primary_key=True)
    phone_number = PostgresUtils.db.Column(PostgresUtils.db.String(20), unique=True, nullable=False)
    name = PostgresUtils.db.Column(PostgresUtils.db.String(100), nullable=False)
    language = PostgresUtils.db.Column(PostgresUtils.db.String(50), nullable=False)
    created_at = PostgresUtils.db.Column(PostgresUtils.db.DateTime, default=datetime.utcnow)
    updated_at = PostgresUtils.db.Column(PostgresUtils.db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, phone_number: str, name: str, language: str, id: int = None):
        self.id = id
        self.phone_number = phone_number
        self.name = name
        self.language = language
