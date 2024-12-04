from typing import TypedDict, List
from datetime import datetime
from domain.models.farm import Farm

class FarmCreateRequest(TypedDict):
    area: float
    village: str
    crop_grown: str
    sowing_date: str  # Format: YYYY-MM-DD
    farmer_id: int

class FarmUpdateRequest(TypedDict, total=False):
    area: float
    village: str
    crop_grown: str
    sowing_date: str
    farmer_id: int

class FarmResponse(TypedDict):
    id: int
    area: float
    village: str
    crop_grown: str
    sowing_date: str
    farmer_id: int

class FarmDTOMapper:
    @staticmethod
    def to_domain(request: FarmCreateRequest) -> Farm:
        return Farm(
            area=request['area'],
            village=request['village'],
            crop_grown=request['crop_grown'],
            sowing_date=datetime.strptime(request['sowing_date'], '%Y-%m-%d').date(),
            farmer_id=request['farmer_id']
        )
    
    @staticmethod
    def to_response(farm: Farm) -> FarmResponse:
        return {
            'id': farm.id,
            'area': farm.area,
            'village': farm.village,
            'crop_grown': farm.crop_grown,
            'sowing_date': farm.sowing_date.isoformat(),
            'farmer_id': farm.farmer_id
        }
    
    @staticmethod
    def to_response_list(farms: List[Farm]) -> List[FarmResponse]:
        return [FarmDTOMapper.to_response(f) for f in farms]
