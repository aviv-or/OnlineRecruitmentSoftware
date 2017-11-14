from enum import Enum


# Login and Register

class LoginResult(Enum):
    SOMETHING_ELSE = {"type":"danger", "message":"Something Looks Wrong"}
    WRONG_USERNAME_OR_PASSWORD = {"type":"danger", "message":"Wrong Username or Password"}
    ORGANIZATION_NOT_VERIFIED = {"type":"warning", "message":"Organization Not Yet Verified"}

class RegisterResult(Enum):
    NONE = {"type":"success", "message":"Registered Successfully"}
    SOMETHING_ELSE = {"type":"danger", "message":"Something Looks Wrong"}
    EMAIL_ALREADY_EXISTS = {"type":"warning", "message":"Email already exists"}

# Organization

class AddResult(Enum):
    ADDED = {"type":"success", "message":"Added Successfully"}
    SOMETHING_ELSE = {"type":"danger", "message":"Something Looks Wrong"}
    EMP_NOT_VALID = {"type":"warning", "message":"User Does Not Exist"}
    EMP_NOT_FREE = {"type":"warning", "message":"User already belongs to some organization"}

class RemoveResult(Enum):
    REMOVED = {"type":"success", "message":"Removed Successfully"}
    SOMETHING_ELSE = {"type":"danger", "message":"Something Looks Wrong"}
    EMP_NOT_VALID = {"type":"warning", "message":"User Does Not Exist"}

# Employees

class CreatePSetResult(Enum):
    ADDED = {"type":"success", "message":"Added Successfully"}
    SOMETHING_ELSE = {"type":"danger", "message":"Something Else"}
    NO_QUESTIONS = {"type":"warning", "message":"No Question in Problem Set"}
    NO_NAME = {"type":"warning", "message":"No Name in Problem Set"}
    SAME_NAME_EXISTS = {"type":"warning", "message":"Problem Sets with same name exists"}

class CreateTMResult(Enum):
    ADDED = {"type":"success", "message":"Added Successfully"}
    SOMETHING_ELSE = {"type":"danger", "message":"Something Looks Wrong"}
    
    NO_PSET = {"type":"warning", "message":"No Problem Sets added"}
    NO_NAME = {"type":"warning", "message":"No Name in Problem Set"}
    SAME_NAME_EXISTS = {"type":"warning", "message":"Test Module with this name exists"}

    WRONG_DATE = {"type":"warning", "message":"No Or Wrong Date Provided"}
    WRONG_TIME = {"type":"warning", "message":"No or Wrong Time Provided"}
    WRONG_DURATION = {"type":"warning", "message":"No Or Wrong Duration Provided"}

    NO_POSITION = {"type":"warning", "message":"No Position Provided"}
    WRONG_JOB_DURATION = {"type":"warning", "message":"No or Wrong Job Duration Provided"}
    WRONG_JOB_TYPE = {"type":"warning", "message":"No or Wrong Job Type Provided"}