from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class FarmerHelper:
    phone_number: str
    name: str
    language: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Errors:
        DUPLICATE_PHONE = {
            "msg": "Phone number already exists",
            "status_code": 400,
            "additional_info": {
                "error_type": "CLIENT",
                "error_name": "DUPLICATE_PHONE"
            }
        }
        
        FARMER_NOT_FOUND = {
            "msg": "Farmer not found",
            "status_code": 404,
            "additional_info": {
                "error_type": "CLIENT",
                "error_name": "FARMER_NOT_FOUND"
            }
        }

    def validate(self) -> bool:
        # Add any validation logic here
        return True
