import enum

class SubmissionSetData(dict):

    def __init__(self):
        self['_id']             = None
        self['test']            = None
        self['submissions']     = {}

    def load(self, data):
        self['_id']             = data.get('_id')
        self['test']            = data.get('test')
        self['submissions']     = data.get('submissions')

    def valid(self, submission=False):
        self.error = self.Error.NONE

        if not self.get('test'):
            self.error = self.Error.TEST

        if self.error != self.Error.NONE:
            return False

        return True

    class Error(enum.Enum):
        NONE                    = "None"
        DOES_NOT_EXIST          = "Does Not Exist"
        TEST                    = "Does Not Belong to any Test"
        SUBMISSIONS             = "Includes Wrong Submissions"