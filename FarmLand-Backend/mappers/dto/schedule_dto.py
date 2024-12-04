from typing import TypedDict, List
from domain.models.schedule import Schedule

class ScheduleCreateRequest(TypedDict):
    days_after_sowing: int
    fertilizer_type: str
    quantity: float
    quantity_unit: str
    farm_id: int

class ScheduleUpdateRequest(TypedDict, total=False):
    days_after_sowing: int
    fertilizer_type: str
    quantity: float
    quantity_unit: str
    farm_id: int

class ScheduleResponse(TypedDict):
    id: int
    days_after_sowing: int
    fertilizer_type: str
    quantity: float
    quantity_unit: str
    farm_id: int

class ScheduleDTOMapper:
    @staticmethod
    def to_domain(request: ScheduleCreateRequest) -> Schedule:
        return Schedule(
            days_after_sowing=request['days_after_sowing'],
            fertilizer_type=request['fertilizer_type'],
            quantity=request['quantity'],
            quantity_unit=request['quantity_unit'],
            farm_id=request['farm_id']
        )
    
    @staticmethod
    def to_response(schedule: Schedule) -> ScheduleResponse:
        return {
            'id': schedule.id,
            'days_after_sowing': schedule.days_after_sowing,
            'fertilizer_type': schedule.fertilizer_type,
            'quantity': schedule.quantity,
            'quantity_unit': schedule.quantity_unit,
            'farm_id': schedule.farm_id
        }
    
    @staticmethod
    def to_response_list(schedules: List[Schedule]) -> List[ScheduleResponse]:
        return [ScheduleDTOMapper.to_response(s) for s in schedules]
