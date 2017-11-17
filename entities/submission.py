from db.interface.submission import SubmissionData

class Submission(SubmissionData):
    def __init__(self, data=None):
        super().__init()

        if data:
            super().load(data)

    def test(self):
        from db.test_module_database import TestModuleDB
        test_id = self.get('test')
        return TestModuleDB(uno=test_id)

    def user(self):
        from db.user_database import UserDB
        user_id = self.get('user')
        return UserDB(uno=user_id)

    def response(self, pset_id, q_no):
        pset = self['responses'].get(pset_id)
        if not pset:
            return None
        return pset.get(q_no)

    def valid(self, safe=True):
        if not super().valid():
            return False

        if safe:
            if not self.get('id'):
                self.error = self.Error.DOES_NOT_EXIST
                return False

        return True
