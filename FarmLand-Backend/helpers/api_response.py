from typing import Any, Optional
from dataclasses import dataclass

@dataclass
class ErrorAdditionalInfo:
    error_type: str
    error_name: str

@dataclass
class Error:
    msg: str
    status_code: int
    additional_info: ErrorAdditionalInfo

@dataclass
class ApiResponse:
    data: Any
    msg: str
    error: Optional[Error] = None

    def __init__(self, data=None, msg="", error=None):
        self.data = data
        self.msg = msg
        self.error = error
