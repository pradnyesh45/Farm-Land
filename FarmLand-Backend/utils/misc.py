from uuid import uuid4
from typing import Any, Dict, Optional
from helpers.api_response import ApiResponse, Error
from flask import g

class MiscUtils:
    @staticmethod
    def generate_uuid4() -> str:
        return str(uuid4())

    @staticmethod
    def get_new_filtered_dict(original: Dict, filter_dict: Dict) -> Dict:
        return {k: v for k, v in original.items() if k in filter_dict}

    @staticmethod
    def auth_data(error_out: bool = True) -> tuple[Optional[Any], Optional[str]]:
        user = getattr(g, 'user', None)
        token = getattr(g, 'token', None)
        if error_out and (not user or not token):
            raise Exception("Unauthorized")
        return user, token
