from enum import Enum
from datetime import datetime, date, timedelta

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
        return OrganizationDB.organization(uno=self.get('organization'))

    def problem_sets(self):
        from entities.problem_set import ProblemSet
        psetdb = ProblemSetDB.all()
        psets = [doc for doc in psetdb if doc['_id'] in self['problem_sets']]
        return psets

    def status(self):
        if self.is_completed():
            return self.Status.COMPLETED
        elif self.is_live():
            return self.Status.LIVE
        else:
            return self.Status.UPCOMING

    def is_live(self):
        now = datetime.now()

        if not self.get('schedule'):
            return False

        test_date = self['schedule']['date']
        test_time = self['schedule']['time']
        test_duration = self['schedule']['duration']

        tdatetime = datetime.strptime(test_date+"-"+test_time, "%d-%m-%Y-%H:%M")

        if tdatetime > now:
            return False

        if tdatetime + timedelta(minutes=int(test_duration)+1) < now:
            return False

        return True

    def is_completed(self):
        days, hours, minutes = self.remaining_time(True)
        if days == 0 and hours == 0 and minutes == 0:
            return True

        return False

    def pretty_date(self, include_duration=False, year=True):
        test_date_time = self['schedule']['date']+"-"+self['schedule']['time']
        test_date_time = datetime.strptime(test_date_time, "%d-%m-%Y-%H:%M")

        if include_duration:
            test_date_time += timedelta(minutes=int(self['schedule']['duration']))

        if year:
            return test_date_time.strftime("%d %B %Y")
        else:
            return test_date_time.strftime("%d %B")

    def pretty_remaining_time(self):
        days, hours, minutes = self.remaining_time()
        result = ""
        if days != 0:
            result += str(days) + "d "
        result += str(hours)+"h "+str(minutes)+"m"
        return result

    def remaining_time(self, include_duration = False):
        test_date_time = self['schedule']['date']+"-"+self['schedule']['time']
        test_date_time = datetime.strptime(test_date_time, "%d-%m-%Y-%H:%M")
        now = datetime.now()

        if include_duration:
            end_test_date_time = test_date_time + timedelta(minutes=int(self['schedule']['duration'] ) + 1)
        else:
            end_test_date_time = test_date_time

        if now > end_test_date_time:
            return 0,0,0

        difference = end_test_date_time - now

        days = difference.days
        hours = difference.seconds//3600 - difference.days*24
        minutes = difference.seconds//60 - hours*60

        return days, hours, minutes

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

    class Status(Enum):
        COMPLETED = "Completed"
        LIVE = "Live"
        UPCOMING = "Upcoming"