from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class FarmHelper:
    farmer_id: int
    area: float
    village: str
    crop_grown: str
    sowing_date: datetime
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Errors:
        FARM_NOT_FOUND = {
            "msg": "Farm not found",
            "status_code": 404,
            "additional_info": {
                "error_type": "CLIENT",
                "error_name": "FARM_NOT_FOUND"
            }
        }

    def validate(self) -> bool:
        if self.area <= 0 or not self.village or not self.crop_grown or not self.sowing_date:
            raise Exception("Invalid farm data")
        return True
