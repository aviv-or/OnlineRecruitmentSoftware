from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.views import View

from db.test_module_database import TestModuleDB
from db.user_database import UserDB

from default import TEST_MODULES, JobDuration, JobType
from default import AUTH_RESULT, LOGIN_ID, LOGIN_TYPE, LoginType

import testhelper

class BrowseTest(View):
    def get(self, request):
        context = {}
        login_id = None
        if LOGIN_ID in request.session :
            login_id = request.session[LOGIN_ID]

        login_type = None
        if LOGIN_TYPE in request.session :
            login_type = request.session[LOGIN_TYPE]

        if login_id and login_type:
            if login_type == LoginType.ORG:
                org = OrganizationDB.organization(uno=login_id)
                if org.valid():
                    context['org'] = org
                    context['login'] = True

            elif login_type == LoginType.EMP:
                user = UserDB.user(uno=login_id)
                if user.valid():
                    context['user'] = user
                    context['login'] = True

        return render(request, "test/browse.html", context)

class ViewTest(View):
    def get(self, request, test_id):
        context = {}
        login_id = None
        if LOGIN_ID in request.session :
            login_id = request.session[LOGIN_ID]

        login_type = None
        if LOGIN_TYPE in request.session :
            login_type = request.session[LOGIN_TYPE]

        if login_id and login_type:
            if login_type == LoginType.ORG:
                org = OrganizationDB.organization(uno=login_id)
                if org.valid():
                    context['org'] = org
                    context['login'] = True

            elif login_type == LoginType.EMP:
                user = UserDB.user(uno=login_id)
                if user.valid():
                    context['user'] = user
                    context['login'] = True

        test = TestModuleDB.test_module(uno=test_id)
        if not test.valid():
            raise Http404

        test['id'] = test['_id']
        test['organization'] = test.organization()

        job_type = test['job_offer']['type']
        for jt in JobType:
            if job_type == jt.name:
                test['job_offer']['type'] = jt.value
                break;

        job_duration = test['job_offer']['duration']
        for jd in JobDuration:
            if job_duration == jd.name:
                test['job_offer']['duration'] = jd.value
                break;

        if testhelper.is_completed_test(test):
            test['status'] = "completed"
        elif testhelper.is_live_test(test):
            test['status'] = "live"
            days, hours, minutes = testhelper.remaining_time(test)
            time = ""
            if days != 0:
                time += str(days) + "d "
            time += str(hours)+"h "+str(minutes)+"m"
            test['remaining_time'] = time
        else:
            test['status'] = "coming"
            days, hours, minutes = testhelper.remaining_time(test, live=False)
            time = ""
            if days != 0:
                time += str(days) + "d "
            time += str(hours)+"h "+str(minutes)+"m"
            test['remaining_time'] = time

        test_duration = int(test['schedule']['duration'])
        if test_duration/60 <= 1:
            test['schedule']['duration'] = str(test_duration) + "min"
        else:
            test['schedule']['duration'] = str(test_duration/60) + "h"

        test['schedule']['date'] = testhelper.pretty_date(test)
        context['test'] = test

        return render(request, "test/view.html", context)
