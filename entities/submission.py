from db.interface.submission import SubmissionData

class Submission(SubmissionData):
    def __init__(self, data=None):
        super().__init__()

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
        return pset.get(str(q_no))

    def save_response(self, pset_id, q_no, answer):
        if self['responses'].get(pset_id):
            self['responses'][pset_id][q_no] = answer
        else:
            self['responses'][pset_id] = {q_no: answer}

    def valid(self, safe=True):
        if not super().valid():
            return False

        if safe:
            if not self.get('_id'):
                self.error = self.Error.DOES_NOT_EXIST
                return False

        return True
