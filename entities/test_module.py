from db.interface.test_module_data import TestModuleData
from db.problem_set_database import ProblemSetDB
from db.submission_set_database import SubmissionSetDB

class TestModule(TestModuleData):
    def __init__(self, data=None):
        super().__init__()

        if data:
            self.load(data)

    def organization(self):
        from db.organization_database import OrganizationDB
        return OrganizationDB.organization(id=self.get('organization'))

    def problem_sets(self):
        from entities.problem_set import ProblemSet
        psetdb = ProblemSetDB.all()
        psets = [doc for doc in psetdb if doc['_id'] in self['problem_sets']]
        return psets

    def submissions(self):
        submissions = self.get('submissions')
        return SubmissionSetDB.submission_set(uno=submissions)

    def valid(self, safe=True, schedule=False, job=False):
        if not super().valid(schedule, job):
            print("Test Module Error : "+self.error.value)
            return False

        if safe:
            if not self.get('_id'):
                self.error = self.Error.DOES_NOT_EXIST
                print("Test Module Error : "+self.error.value)
                return False

        all_psets = self.get('problem_sets', [])
        psets = ProblemSetDB.all()
        psets = {doc['_id']:doc for doc in psets}

        for pset in all_psets:
            if pset not in psets:
                self.error = self.Error.PSET_DOES_NOT_EXIST
                print("Test Module Error : "+self.error.value)
                return False

        return True