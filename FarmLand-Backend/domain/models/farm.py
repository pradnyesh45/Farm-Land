from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Farm:
    area: float
    village: str
    crop_grown: str
    sowing_date: date
    farmer_id: int
    id: Optional[int] = None
