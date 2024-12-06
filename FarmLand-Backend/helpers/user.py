from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from helpers.auth import UserRole

@dataclass
class UserHelper:
    username: str
    role: str
    id: Optional[int] = None
    password: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Errors:
        INVALID_CREDENTIALS = {
            "msg": "Invalid credentials",
            "status_code": 401,
            "additional_info": {
                "error_type": "CLIENT",
                "error_name": "INVALID_CREDENTIALS"
            }
        }
        
        DUPLICATE_USERNAME = {
            "msg": "Username already exists",
            "status_code": 400,
            "additional_info": {
                "error_type": "CLIENT",
                "error_name": "DUPLICATE_USERNAME"
            }
        }

    def validate_role(self) -> bool:
        return self.role in [role.value for role in UserRole]
