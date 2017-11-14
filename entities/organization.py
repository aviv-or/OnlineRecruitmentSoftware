from datetime import date, datetime, timedelta

from db.interface.organization_data import OrganizationData
from db.test_module_database import TestModuleDB
from db.problem_set_database import ProblemSetDB
from .test_module import TestModule
from .problem_set import ProblemSet

class Organization(OrganizationData):
    def __init__(self, data=None):

        super().__init__()

        if data:
            super().load(data)

    def valid(self, safe=True):
        if not super().valid():
            print("Organization Error : "+self.error.value)
            return False

        if safe:
            if not self.get('_id'):
                self.error = self.Error.DOES_NOT_EXIST
                print("Organization Error : "+self.error.value)
                return False

        return True

    def employees(self, etype=None):
        from db.user_database import UserDB
        from .user import User
        if etype == self.EmpType.GN:
            userdb = UserDB.all()
            role = self.EmpType.GN
            gn_arr = self.get('employees')[role.name]
            return [User(doc) for doc in userdb if doc['_id'] in gn_arr and doc['role'] == role.name]

        elif etype == self.EmpType.HR:
            return UserDB.user(uno=self.get('employees')[self.EmpType.HR.name])

        elif etype == self.EmpType.SU:
            return UserDB.user(uno=self.get('employees')[self.EmpType.SU.name])

        elif etype == self.EmpType.PS:
            return UserDB.user(uno=self.get('employees')[self.EmpType.PS.name])

        return User()

    def tests(self):
        testdb = TestModuleDB.all()
        tests = [TestModule(doc) for doc in testdb if doc['_id'] in self['test_modules']]
        return tests

    def problem_sets(self):
        psetdb = ProblemSetDB.all()
        psets = [ProblemSet(doc) for doc in psetdb if doc['_id'] in self['problem_sets']]
        return psets

    def scheduled_tests(self):
        testdb = TestModuleDB.all()
        tests = [TestModule(doc) for doc in testdb if doc['_id'] in self['test_modules'] and doc['schedule']]
        return tests

    def active_tests(self):
        testdb = TestModuleDB.all()
        tests = [TestModule(doc) for doc in testdb if doc['_id'] in self['test_modules'] and doc['schedule']]

        return tests

        # TODO find active tests
        active = []
        dt = datetime.now()

        for test in tests:
            schedule = test.get('schedule')
            if schedule.valid():
                da = schedule['date']
                da = datetime.strptime(da, "%d-%m-%Y").date()

    def verified(self):
        return self.get('verified', False)

    def add(self,emp):
        self['employees']['GN'].append(emp)

    def remove(self, emp):
        self['employees']['GN'].remove(emp)

    def set_emp(self, emptype, emp):
        if emptype == self.EmpType.HR:
            self['employees']['GN'].remove(emp)
            self['employees']['HR'] = emp

        if emptype == self.EmpType.SU:
            self['employees']['GN'].remove(emp)
            self['employees']['SU'] = emp

        if emptype == self.EmpType.PS:
            self['employees']['GN'].remove(emp)
            self['employees']['PS'] = emp

    def remove_emp(self, emptype):
        if emptype == self.EmpType.HR:
            self['employees']['HR'] = None

        if emptype == self.EmpType.SU:
            self['employees']['SU'] = None

        if emptype == self.EmpType.PS:
            self['employees']['PS'] = None