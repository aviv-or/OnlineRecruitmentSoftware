import enum

from .organization_data import OrganizationData
from entities.submission import Submission

class UserData(dict):

    def __init__(self):
        self['_id']             = None
        self['name']            = None
        self['email']           = None
        self['description']     = None
        self['website']         = None
        self['password']        = None
        self['organization']    = None
        self['role']            = None
        self['submissions']     = {}

    def load(self, data):
        self['_id']             = data.get('_id')
        self['name']            = data.get('name')
        self['email']           = data.get('email')
        self['description']     = data.get('description')
        self['website']         = data.get('website')
        self['password']        = data.get('password')
        self['organization']    = data.get('organization')
        self['role']            = data.get('role')
        self['submissions']     = data.get('submissions', {})

    def valid(self):
        self.error = self.Error.NONE

        if not self.get('name'):
            self.error = self.Error.NAME

        elif not self.get('email'):
            self.error = self.Error.EMAIL

        elif not self.get('password'):
            self.error = self.Error.PASSWORD

        if self.get('organization'):
            if self.get('role') not in [ty.name for ty in OrganizationData.EmpType]:
                self.error = self.Error.ROLE

        if self.error != self.Error.NONE:
            return False

        return True

    class Error(enum.Enum):
        NONE                    = "None"
        DOES_NOT_EXIST          = "Does Not Exist"
        NAME                    = "No or Wrong Name"
        EMAIL                   = "No or Wrong Email"
        PASSWORD                = "No or Wrong Password"
        EMAIL_ALREADY_EXISTS    = "Email Already Exists"
        SUBMISSIONS             = "Includes Wrong Submissions"
        ROLE                    = "Unknown Role"