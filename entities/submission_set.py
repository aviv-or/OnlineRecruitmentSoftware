from db.interface.submission_set import SubmissionSetData

class SubmissionSet(SubmissionSetData):
    def __init__(self, data=None):
        super().__init()

        self.loaded = False
        self.submissions = {}

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

    def load_submissions(self):
        from db.submission_database import SubmissionDB
        subs = data.get('submissions', {})
        sub_dict = {}
        for key, value in subs:
            sub_dict[key] = SubmissionDB.submission(uno=value)
        self.submissions = sub_dict
        self.loaded = True

    def submission(self, user_id=None):
        if not user_id:
            return None

        if self.loaded:
            return self.submissions.get(user_id)
        else:
            subs = self.get('submissions')
            sub_id = subs.get(user_id)
            return SubmissionDB(uno=sub_id)

    def all_submissions(self):
        if not self.loaded:
            self.load_submissions()
        
        return [sub for user,sub in self.submissions]

    def add(self, user, submission):
        subs = self.get('submissions')
        subs[user] = submission

    def valid(self, safe=True):
        if not super().valid():
            return False

        if safe:
            if not self.get('id'):
                self.error = self.Error.DOES_NOT_EXIST
                return False

        return True
