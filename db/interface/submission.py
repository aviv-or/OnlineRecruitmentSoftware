from enum import Enum

class SubmissionData(dict):

    def __init__(self):
        self['_id']             = None
        self['test']            = None
        self['user']            = None
        self['responses']       = {}

    def load(self, data):
        self['_id']             = data.get('_id')
        self['test']            = data.get('test')
        self['user']            = data.get('user')
        self['responses']       = data.get('responses', {})

    def valid(self):
        self.error = self.Error.NONE

        if not self.get('test'):
            self.error = self.Error.TEST

        elif not self.get('user'):
            self.error = self.Error.USER

        if self.error != self.Error.NONE:
            return False

        return True

    class Error(Enum):
        NONE                    = "None"
        DOES_NOT_EXIST          = "Does Not Exist"
        USER                    = "Doesn't Belong To a User"
        TEST                    = "Doesn't Belong To a Test"