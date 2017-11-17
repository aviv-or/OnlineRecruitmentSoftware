from enum import IntEnum, Enum

# Type Of Users

class LoginType(IntEnum):
    ORG = 1
    EMP = 2

# Login Cookies

ADMIN_ID = 'admin_id'

LOGIN_ID = 'user_id'
LOGIN_TYPE = 'user_type'

# Cookies

AUTH_RESULT = 'auth_result'

ADD_EMP_RESULT = 'add_emp_result'
REMOVE_EMP_RESULT = "remove_emp_result"
ADD_PROBLEM_SET_RESULT = 'add_ps_result'
ADD_TEST_MODULE_RESULT = 'add_tm_result'
SCHEDULE_TEST_MODULE_RESULT = 'schedule_tm_result'

# databases

ADMIN = "admin"
USERS = "users"
ORGANIZATIONS = "organizations"
PROBLEM_SETS = "problem_sets"
TEST_MODULES = "test_modules"
SUBMISSIONS = "submissions"
SUBMISSION_SETS = "submission_sets"
# USERS = "test_user"
# ORGANIZATIONS = "test_organization"
# PROBLEM_SETS = "test_pset"
# TEST_MODULES = "test_test_module"
# SUBMISSIONS = "test_submissions"
# SUBMISSION_SETS = "test_submission_sets"

# employee types

GENERAL_MEMBER = "GN"
TEST_SUPERVISOR = "SU"
HR_MANAGER = "HR"
PROBLEM_SETTER = "PS"
