import enum

class SubmissionData(dict):

    def __init__(self):
        self['_id']             = None
        self['test']            = None
        self['user']            = None
        self['responses']       = None

    def load(self, data):
        self['_id']             = data.get('_id')
        self['test']            = data.get('test')
        self['user']            = data.get('user')
        self['responses']       = data.get('responses')

    def valid(self):
        self.error = self.Error.NONE

        if not self.get('test'):
            self.error = self.Error.TEST

        elif not self.get('user'):
            self.error = self.Error.USER

        elif not self.get('responses'):
            self.error = self.Error.RESPONSES

        if self.error != self.Error.NONE:
            return False

        return True

    class Error(enum.Enum):
        NONE                    = "None"
        DOES_NOT_EXIST          = "Does Not Exist"
        USER                    = "Doesn't Belong To a User"
        TEST                    = "Doesn't Belong To a Test"
        RESPONSES               = "Doesn't have any Responses"