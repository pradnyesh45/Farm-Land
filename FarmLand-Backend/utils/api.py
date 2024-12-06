from flask import jsonify
from helpers.api_response import ApiResponse, Error, ErrorAdditionalInfo

class ApiUtils:
    @staticmethod
    def get_api_response(api_response: ApiResponse):
        response = {
            "success": api_response.error is None,
            "msg": api_response.msg if api_response.error is None else api_response.error.msg,
            "data": api_response.data if api_response.error is None else None
        }
        
        if api_response.error:
            response["error"] = {
                "type": api_response.error.additional_info.error_type,
                "name": api_response.error.additional_info.error_name
            }
        
        status_code = 200 if api_response.error is None else api_response.error.status_code
        return jsonify(response), status_code

    @staticmethod
    def get_error_response(error):
        if isinstance(error, dict):
            return ApiUtils.get_api_response(ApiResponse(
                data=None,
                msg=error.get('msg', 'Unknown error'),
                error=Error(
                    msg=error.get('msg', 'Unknown error'),
                    status_code=error.get('status_code', 500),
                    additional_info=ErrorAdditionalInfo(
                        error_type=error.get('additional_info', {}).get('error_type', 'SERVER'),
                        error_name=error.get('additional_info', {}).get('error_name', 'UNKNOWN_ERROR')
                    )
                )
            ))
        else:
            return ApiUtils.get_api_response(ApiResponse(
                data=None,
                msg=str(error),
                error=Error(
                    msg=str(error),
                    status_code=500,
                    additional_info=ErrorAdditionalInfo(
                        error_type="SERVER",
                        error_name="INTERNAL_SERVER_ERROR"
                    )
                )
            ))
