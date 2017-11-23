from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.views import View

from db.test_module_database import TestModuleDB
from db.user_database import UserDB

from default import TEST_MODULES, JobDuration, JobType
from default import AUTH_RESULT, LOGIN_ID, LOGIN_TYPE, LoginType

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
                    user_name_arr = user['name'].split()
                    user_init = ""
                    for i in user_name_arr:
                        user_init += i[0]
                    user['initial'] = user_init
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
                    user_name_arr = user['name'].split()
                    user_init = ""
                    for i in user_name_arr:
                        user_init += i[0]
                    user['initial'] = user_init
                    user['organization'] = user.organization()
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

        if test.is_completed():
            test['status'] = "completed"
        elif test.is_live():
            test['status'] = "live"
            test['remaining_time'] = test.pretty_remaining_time(True)
        else:
            test['status'] = "coming"
            test['remaining_time'] = test.pretty_remaining_time()

        test_duration = int(test['schedule']['duration'])
        if test_duration/60 <= 1:
            test['schedule']['duration'] = str(test_duration) + "min"
        else:
            test['schedule']['duration'] = str(test_duration/60) + "h"

        test['schedule']['open_date'] = test.pretty_date()
        context['test'] = test

        return render(request, "test/view.html", context)

class StartTest(View):
    def get(self, request, test_id):
        context = {}
        found_sub = None
        login_id = request.session.get(LOGIN_ID)
        login_type = request.session.get(LOGIN_TYPE)

        test = TestModuleDB.test_module(uno=test_id)
        if not test.valid():
            return Http404

        if not test.is_live():
            return HttpResponseRedirect("/test/"+test_id)

        if not login_id or not login_type:
            return HttpResponseRedirect("/login?r=/test/start/"+test_id)

        if login_type == LoginType.ORG:
            org = OrganizationDB.organization(uno=login_id)
            if org.valid():
                context['org'] = org
                context['login'] = True
            else:
                del request.session[LOGIN_ID]
                request.session[AUTH_RESULT] = LoginResult.SOMETHING_ELSE
                return HttpResponseRedirect("/login?r=/test/start/"+test_id)

        elif login_type == LoginType.EMP:
            user = UserDB.user(uno=login_id)
            if user.valid():
                user_name_arr = user['name'].split()
                user_init = ""
                for i in user_name_arr:
                    user_init += i[0]
                user['initial'] = user_init
                context['user'] = user
                context['login'] = True
            else:
                del request.session[LOGIN_ID]
                request.session[AUTH_RESULT] = LoginResult.SOMETHING_ELSE
                return HttpResponseRedirect("/login?r=/test/start/"+test_id)

            if not user['role'] or not user['organization']:
                context['pe'] = True
                submission = user.submission(test=test_id)
                if submission.valid():
                    found_sub = submission
                elif user.register_for_test(test=test):
                    TestModuleDB.update(test)
                    UserDB.update(user)

        test['id'] = test['_id']
        count = 1
        problem_sets = test.problem_sets()
        for pset in problem_sets:
            pset['no'] = count
            pset['id'] = pset['_id']
            count = count + 1
            if found_sub:
                for q in pset['questions']:
                    q['submitted_data'] = submission.response(pset['_id'], q['no'])

        test['problem_sets'] = problem_sets
        test['remaining_time'] = test.pretty_remaining_time(True)
        context['test'] = test
        return render(request, "test/start.html", context)

    def post(self, request):
        pass