from enum import IntEnum

class LoginError(IntEnum):
    NONE = 1
    SOMETHING_ELSE = 2
    WRONG_USERNAME_OR_PASSWORD = 3
    ORGANIZATION_NOT_VERIFIED = 4

class RegisterError(IntEnum):
    NONE = 101
    SOMETHING_ELSE = 102
    USER_ALREADY_EXISTS = 103
    ORGANIZATION_ALREADY_EXISTS = 104