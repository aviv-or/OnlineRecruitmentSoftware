from enum import Enum

class OrganizationData(dict):

    def __init__(self):
        self['_id']          = None
        self['name']         = None
        self['email']        = None
        self['description']  = None
        self['password']     = None
        self['website']      = None
        self['category']     = None
        self['location']     = None
        self['employees']    = {'HR':None, 'SU':None, 'PS':None, 'GN':[]}
        self['problem_sets'] = []
        self['test_modules'] = []
        self['verified']     = False

    def load(self, data):
        self['_id']          = data.get('_id')
        self['name']         = data.get('name')
        self['email']        = data.get('email')
        self['password']     = data.get('password')
        self['description']  = data.get('description')
        self['website']      = data.get('website')
        self['category']     = data.get('category')
        self['location']     = data.get('location')
        empl = {'HR':None, 'SU':None, 'PS':None, 'GN':[]}
        self['employees']    = data.get('employees', empl)
        self['problem_sets'] = data.get('problem_sets', [])
        self['test_modules'] = data.get('test_modules', [])
        self['verified']     = data.get('verified', False)

    def valid(self):
        self.error = self.Error.NONE
        if not self.get('name'):
            self.error = self.Error.NAME

        elif not self.get('email'):
            self.error = self.Error.EMAIL

        elif not self.get('password'):
            self.error = self.Error.PASSWORD

        elif not self.get('website'):
            self.error = self.Error.WEBSITE

        elif not self.get('location'):
            self.error = self.Error.LOCATION

        if self.error != self.Error.NONE:
            return False

        return True

    class Error(Enum):
        NONE                 = "NONE"
        DOES_NOT_EXIST       = "DOES_NOT_EXIST"
        NAME                 = "NAME"
        EMAIL                = "EMAIL"
        WEBSITE              = "WEBSITE"
        LOCATION             = "LOCATION"
        CATEGORY             = "CATEGORY"
        PASSWORD             = "PASSWORD"
        EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"

    class EmpType(Enum):
        HR = "Human Resource"
        SU = "Supervisor"
        PS = "Problem Setter"
        GN = "General Member"