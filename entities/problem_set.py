from db.interface.problem_set_data import ProblemSetData, Question

class ProblemSet(ProblemSetData):
    def __init__(self, data=None):
        super().__init__()

        if data:
            self.load(data)

    def organization(self):
        from db.organization_database import OrganizationDB
        if 'organization' in self:
            org = OrganizationDB.organization(uno=self['organization'])
        else:
            org = Organization()

        return org

    def questions(self, qtype):
        ques_arr = []

        for ques in self['questions']:
            if ques.type() == qtype:
                ques_arr.append(ques)

        return ques_arr

    def valid(self, safe=True):
        if not super().valid():
            print("Problem Set Error : "+self.error.value)
            return False

        if safe:
            if not self.get('_id'):
                self.error = self.Error.DOES_NOT_EXIST
                print("Problem Set Error : "+self.error.value)
                return False

        return True
