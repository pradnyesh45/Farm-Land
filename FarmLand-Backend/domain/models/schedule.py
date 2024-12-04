from dataclasses import dataclass
from typing import Optional

@dataclass
class Schedule:
    days_after_sowing: int
    fertilizer_type: str
    quantity: float
    quantity_unit: str
    farm_id: int
    id: Optional[int] = None
