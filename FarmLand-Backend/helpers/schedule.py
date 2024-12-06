from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ScheduleHelper:
    farm_id: int
    days_after_sowing: int
    fertilizer_type: str
    quantity: float
    quantity_unit: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Errors:
        SCHEDULE_NOT_FOUND = {
            "msg": "Schedule not found",
            "status_code": 404,
            "additional_info": {
                "error_type": "CLIENT",
                "error_name": "SCHEDULE_NOT_FOUND"
            }
        }

    def validate(self) -> bool:
        if not self.fertilizer_type or self.quantity <= 0 or self.days_after_sowing < 0:
            raise Exception("Invalid schedule data")
        return True
