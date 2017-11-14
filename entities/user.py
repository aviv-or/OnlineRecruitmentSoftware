from db.interface.user_data import UserData
from db.organization_database import OrganizationDB
from .organization import Organization

class User(UserData):
    def __init__(self, data=None):

        super().__init__()

        self._org = None

        if data:
            super().load(data)

    def organization(self):
        if self._org:
            return self._org

        if 'organization' in self:
            org = OrganizationDB.organization(uno=self['organization'])
            self._org = org
        else:
            org = Organization()

        return org

    def valid(self, safe=True):
        if not super().valid():
            print("User Error : "+self.error.value)
            return False

        if safe:
            if not self.get('_id'):
                self.error = self.Error.DOES_NOT_EXIST
                print("User Error : "+self.error.value)
                return False

        return True