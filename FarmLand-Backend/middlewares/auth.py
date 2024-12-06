from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from helpers.api_response import ApiResponse, Error, ErrorAdditionalInfo
from utils.api import ApiUtils
from jwt.exceptions import ExpiredSignatureError
from helpers.auth import UserRole, AuthEntityType
import logging

def authentication_middleware(allowed_roles):
    """
    Authentication middleware that checks if the user has the required role.
    Role hierarchy defined in AuthEntityType:
    - SUPER_USER = [UserRole.SUPER_USER.value]
    - ADMIN = [UserRole.SUPER_USER.value, UserRole.ADMIN.value]
    - USER = [UserRole.SUPER_USER.value, UserRole.ADMIN.value, UserRole.USER.value]
    """
    def decorator(fn):
        @wraps(fn)
        def decorator_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                user_role = claims["role"]

                if user_role in allowed_roles:
                    return fn(*args, **kwargs)

                error = Error(
                    msg=f"Unauthorized access. User role: {user_role} not in allowed roles: {allowed_roles}",
                    status_code=403,
                    additional_info=ErrorAdditionalInfo(
                        error_type="CLIENT",
                        error_name="UNAUTHORIZED"
                    )
                )
                return ApiUtils.get_api_response(ApiResponse(
                    data=None,
                    msg=f"Unauthorized access. User role: {user_role} not in allowed roles: {allowed_roles}",
                    error=error
                ))

            except ExpiredSignatureError:
                error = Error(
                    msg="Your session has expired. Please login again.",
                    status_code=401,
                    additional_info=ErrorAdditionalInfo(
                        error_type="CLIENT",
                        error_name="SESSION_EXPIRED"
                    )
                )
                return ApiUtils.get_api_response(ApiResponse(
                    data=None,
                    msg="Your session has expired. Please login again.",
                    error=error
                ))
            except Exception as e:
                error = Error(
                    msg=str(e),
                    status_code=401,
                    additional_info=ErrorAdditionalInfo(
                        error_type="CLIENT",
                        error_name="AUTHENTICATION_ERROR"
                    )
                )
                return ApiUtils.get_api_response(ApiResponse(
                    data=None,
                    msg="Authentication failed. Please login again.",
                    error=error
                ))
        return decorator_function
    return decorator 