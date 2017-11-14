from enum import Enum

class TestModuleData(dict):

    def __init__(self):
        self._error = self.Error.DOES_NOT_EXIST
        self['_id']          = None
        self['name']         = None
        self['category']     = None
        self['organization'] = None
        self['problem_sets'] = []
        self['schedule']     = {}
        self['job_offer']    = {}

    def load(self, data):
        self['_id']          = data.get('_id')
        self['name']         = data.get('name')
        self['category']     = data.get('category')
        self['organization'] = data.get('organization')
        self['problem_sets'] = data.get('problem_sets', [])
        if data.get('schedule'):
            self['schedule']     = TestSchedule(data.get('schedule', {}))
        if data.get('job_offer'):
            self['job_offer']    = Job(data.get('job_offer', {}))

    def valid(self, schedule=False, job=False):
        self.error = self.Error.NONE

        if not self.get('name'):
            self.error = self.Error.NO_NAME

        elif not self.get('organization'):
            self.error = self.Error.NO_ORGANIZATION

        elif not self.get('category'):
            self.error = self.Error.NO_CATEGORY

        elif not self.get('category'):
            self.error = self.Error.NO_CATEGORY

        elif schedule and self['schedule'] and not self['schedule'].valid():
            self.error = self.Error.SCHEDULE

        elif job and self['job_offer'] and not self['job_offer'].valid():
            self.error = self.Error.JOB_OFFER

        if self.error != self.Error.NONE:
            return False

        return True

    class Error(Enum):
        NONE                = "None"
        DOES_NOT_EXIST      = "no Id Found"
        NO_NAME             = "No Name Provided"
        NO_ORGANIZATION     = "Does Not Belong to a Organization"
        NO_CATEGORY         = "No Category Provided"
        SCHEDULE            = "Wrong Test Schedule"
        JOB_OFFER           = "Wrong Job Offer"
        PSET_DOES_NOT_EXIST = "Problem Set Does Not Exist"


class TestSchedule(dict):
    def __init__(self, data={}):
        print(data)
        self['date'] = data.get('date')
        self['time']   = data.get('time')
        self['duration'] = data.get('duration')

    def valid(self):
        self.error = self.Error.NONE

        if not self.get('date'):
            self.error = self.Error.DATE

        elif not self.get('time'):
            self.error = self.Error.TIME

        elif not self.get('duration'):
            self.error = self.Error.DURATION

        if self.error != self.Error.NONE:
            return False

        return True

    class Error(Enum):
        NONE     = "NONE"
        DATE     = "DATE"
        TIME     = "TIME"
        DURATION = "DURATION"

    class Duration(Enum):
        HALF     = "30"
        ONE      = "60"
        ONE_HALF = "90"
        TWO      = "120"
        TWO_HALF = "150"
        THREE    = "180"

class Job(dict):
    def __init__(self, data={}):

        self.error = self.Error.NONE

        self['position'] = data.get('position')
        self['salary']   = data.get('salary')
        self['currency'] = data.get('currency')
        self['type']     = data.get('type')
        self['office']   = data.get('office')
        self['duration'] = data.get('duration')

    def valid(self):
        self.error = self.Error.NONE

        if not self['position']:
            self.error = self.Error.POSITION

        elif not self['salary']:
            self.error = self.Error.SALARY

        elif not self['currency']:
            self.error = self.Error.CURRENCY

        elif not self['type']:
            self.error = self.Error.TYPE

        elif not self['duration']:
            self.error = self.Error.DURATION

        elif self['currency'] not in [curr.name for curr in self.Currency]:
            self.error = self.Error.CURRENCY

        elif self['type'] not in [ty.name for ty in self.Type]:
            self.error = self.Error.TYPE

        elif self['duration'] not in [dur.name for dur in self.Duration]:
            self.error = self.Error.Duration

        elif self.error != self.Error.NONE:
            return False

        try:
            if int(self['salary']) <= 0:
                self.error = self.Error.SALARY
                return False

        except Exception as e:
            self.error = self.Error.SALARY
            return False

        return True

    class Error(Enum):
        NONE     = "NONE"
        POSITION = "POSITION"
        SALARY   = "SALARY"
        CURRENCY = "CURRENCY"
        TYPE     = "TYPE"
        DURATION = "DURATION"

    class Currency(Enum):
        INR = "INR"
        USD = "USD"
        GBP = "GBP"
        EUR = "EUR"

    class Type(Enum):
        WFH = "Work From Home"
        OFW = "Office Work"

    class Duration(Enum):
        MI3 = "3 Month Internship"
        MI6 = "6 Month Internship"
        FTE = "Full Time Employment"
