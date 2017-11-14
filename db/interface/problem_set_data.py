from enum import Enum

class Question(dict):

    def __init__(self, data=dict()):

        self.type = None

        self['no']           = data.get('no')
        self['question']     = data.get('question')
        self['type']         = data.get('type')
        self['tag']          = data.get('tag')

    def valid(self):
        if not self.get('no')\
        or not self.get('question')\
        or not self.get('type'):
            return False

        return True

    class Type(Enum):
        OBJ = "OBJ"
        SUB = "SUB"
        COD = "COD"

class Subjective(Question):

    def __init__(self, data=dict()):
        super().__init__(data)

        self.type = Question.Type.SUB

        self['limit'] = data.get('limit')

    def valid(self):
        if not super().valid():
            return False

        return True

        # TODO : enable validity for limit

        if not self.get('limit'):
            return False

        limit = self['limit']
        if int(limit) <= 400:
            return False

        return True

class Objective(Question):

    def __init__(self, data=dict()):
        super().__init__(data)

        self.type = Question.Type.OBJ

        self['marks']        = data.get('marks')
        self['options']      = data.get('options', [])
        self['correct']      = data.get('correct')

    def valid(self):
        if not super().valid():
            return False

        if not self.get('options')\
        or not self.get('correct')\
        or not self.get('marks'):
            print("Objective Question not valid")
            return False

        return True

class Coding(Question):

    def __init__(self, data=dict()):
        super().__init__(data)

        self.type = Question.Type.COD

        self['input']        = data.get('input')
        self['output']       = data.get('output')
        self['time_limit']   = data.get('time_limit')
        self['marks']        = data.get('marks')

    def valid(self):
        if not super().valid():
            return False

        if not self.get('output'):
            return False

        if not self.get('time_limit'):
            return False

        if not self.get('marks'):
            return False

        return True

class ProblemSetData(dict):

    def __init__(self):
        self['_id']          = None
        self['name']         = None
        self['public']       = False
        self['organization'] = None
        self['category']     = None
        self['questions']    = []

    def load(self, data):
        self['_id']          = data.get('_id')
        self['name']         = data.get('name')
        self['public']       = data.get('public', False)
        self['organization'] = data.get('organization')
        self['category']     = data.get('category')

        ques_arr = []

        for ques in data.get('questions', []):
            qtype = ques.get('type')
            if qtype == Question.Type.OBJ.value:
                ques_arr.append(Objective(ques))

            elif qtype == Question.Type.SUB.value:
                ques_arr.append(Subjective(ques))

            else:
                ques_arr.append(Coding(ques))

        self['questions']    = ques_arr

    def valid(self):
        self.error = self.Error.NONE

        if not self.get('name'):
            self.error = self.Error.NAME

        elif not self.get('questions'):
            self.error = self.Error.QUESTION

        elif not self.get('category'):
            self.error = self.Error.CATEGORY

        if self.error != self.Error.NONE:
            return False

        for ques in self.get('questions', []):
            if not ques.valid():
                self.error = self.Error.INCORRECT_QUESTIONS
                return False

        return True

    class Error(Enum):
        NONE                = "None"
        DOES_NOT_EXIST      = "Does Not Exist"
        NAME                = "No or Wrong Name"
        QUESTION            = "No or Wrong Question"
        CATEGORY            = "No or Wrong Category"
        INCORRECT_QUESTIONS = "Has Incorrect Questions"