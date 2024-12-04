from dataclasses import dataclass
from typing import Optional

@dataclass
class Farmer:
    name: str
    phone_number: str
    language: str
    id: Optional[int] = None