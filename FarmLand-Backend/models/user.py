from utils.postgres import PostgresUtils
from utils.misc import MiscUtils
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserModel(PostgresUtils.db.Model):
    __tablename__ = "users"

    id = PostgresUtils.db.Column(PostgresUtils.db.Integer, primary_key=True)
    username = PostgresUtils.db.Column(PostgresUtils.db.String(80), unique=True, nullable=False)
    password_hash = PostgresUtils.db.Column(PostgresUtils.db.String(512), nullable=False)
    role = PostgresUtils.db.Column(PostgresUtils.db.String(20), nullable=False)
    created_at = PostgresUtils.db.Column(PostgresUtils.db.DateTime, default=datetime.utcnow)
    updated_at = PostgresUtils.db.Column(PostgresUtils.db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, username: str, role: str, password: str = None, id: int = None):
        self.id = id
        self.username = username
        self.role = role
        if password:
            self.set_password(password)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
