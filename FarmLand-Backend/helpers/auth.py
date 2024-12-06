from enum import Enum
from typing import List

class UserRole(Enum):
    SUPER_USER = 'SuperUser'
    ADMIN = 'Admin'
    USER = 'User'

class AuthEntityType:
    SUPER_USER = [UserRole.SUPER_USER.value]
    ADMIN = [UserRole.SUPER_USER.value, UserRole.ADMIN.value]
    USER = [UserRole.SUPER_USER.value, UserRole.ADMIN.value, UserRole.USER.value]
