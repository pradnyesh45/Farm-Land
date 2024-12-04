from typing import TypedDict, List
from domain.models.farmer import Farmer

class FarmerCreateRequest(TypedDict):
    name: str
    phone_number: str
    language: str

class FarmerUpdateRequest(TypedDict, total=False):
    name: str
    phone_number: str
    language: str

class FarmerResponse(TypedDict):
    id: int
    name: str
    phone_number: str
    language: str

class FarmerDTOMapper:
    @staticmethod
    def to_domain(request: FarmerCreateRequest) -> Farmer:
        return Farmer(
            name=request['name'],
            phone_number=request['phone_number'],
            language=request['language']
        )
    
    @staticmethod
    def to_response(farmer: Farmer) -> FarmerResponse:
        return {
            'id': farmer.id,
            'name': farmer.name,
            'phone_number': farmer.phone_number,
            'language': farmer.language
        }
    
    @staticmethod
    def to_response_list(farmers: List[Farmer]) -> List[FarmerResponse]:
        return [FarmerDTOMapper.to_response(f) for f in farmers]
