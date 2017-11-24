from datetime import datetime, date, timedelta

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.views import View

from db import authhelper
from db.user_database import UserDB
from db.organization_database import OrganizationDB
from db.problem_set_database import ProblemSetDB
from db.test_module_database import TestModuleDB
from db.submission_set_database import SubmissionSetDB

from entities.user import User
from entities.problem_set import ProblemSet
from entities.organization import Organization

from default import AUTH_RESULT, LOGIN_ID, LOGIN_TYPE, LoginType
from default import ORGANIZATIONS, PROBLEM_SETS, TEST_MODULES
from default import ADD_TEST_MODULE_RESULT, SCHEDULE_TEST_MODULE_RESULT
from default import TEST_SUPERVISOR, PROBLEM_SETTER, ADD_PROBLEM_SET_RESULT
                    

from result import CreatePSetResult, CreateTMResult

class CreateProblemSet(View):
    def get(self, request):
        context = {}
        if LOGIN_ID not in request.session or LOGIN_TYPE not in request.session:
            return HttpResponseRedirect("/profile")

        if request.session[LOGIN_TYPE] == LoginType.ORG:
            return HttpResponseRedirect("/profile")

        user_id = request.session[LOGIN_ID]
        user_type = request.session[LOGIN_TYPE]

        user = UserDB.user(uno = user_id)
        if not user.valid():
            return HttpResponseRedirect("/profile")

        if user['role'] != PROBLEM_SETTER:
            return HttpResponseRedirect("/profile")

        user_name_arr = user['name'].split()
        user_init = ""
        for i in user_name_arr:
            user_init += i[0]
        user['initial'] = user_init
        context['user'] = user

        if ADD_PROBLEM_SET_RESULT in request.session:
            pscode = request.session[ADD_PROBLEM_SET_RESULT]
            context['alert'] = pscode

            del request.session[ADD_PROBLEM_SET_RESULT]

        return render(request, "employee/problem_set.html", context)

    def post(self, request):
        
        # validating client

        if LOGIN_ID not in request.session or LOGIN_TYPE not in request.session:
            return HttpResponseRedirect("/profile")

        if request.session[LOGIN_TYPE] == LoginType.ORG:
            return HttpResponseRedirect("/profile")

        user_id = request.session[LOGIN_ID]
        user_type = request.session[LOGIN_TYPE]

        user = UserDB.user(uno = user_id)
        if not user.valid():
            return HttpResponseRedirect("/profile")

        if user['role'] != PROBLEM_SETTER:
            return HttpResponseRedirect("/profile")

        # validating request

        data = request.POST

        noq = data.get('noq')
        if not noq:
            request.session[ADD_PROBLEM_SET_RESULT] = CreatePSetResult.SOMETHING_ELSE.value
            return HttpResponseRedirect("/create/problem-set")

        if int(noq)  <= 0:
            request.session[ADD_PROBLEM_SET_RESULT] = CreatePSetResult.NO_QUESTIONS.value
            return HttpResponseRedirect("/create/problem-set")

        ps_name = data.get('ps_name')
        if not ps_name:
            request.session[ADD_PROBLEM_SET_RESULT] = CreatePSetResult.NO_NAME.value
            return HttpResponseRedirect("/create/problem-set")

        ps_category = data.get('ps_category')

        pset = {
                    "name": ps_name, 
                    "category": ps_category, 
                    "public": False, 
                    "organization": user['organization'], 
                    "questions": []
                }

        problem_sets = ProblemSetDB.all()

        for pset in problem_sets:
            if ps_name == pset['name'] and user['organization'] == pset['organization']:
                request.session[ADD_PROBLEM_SET_RESULT] = CreatePSetResult.SAME_NAME_EXISTS.value
                return HttpResponseRedirect("/create/problem-set")

        allques = []

        for q in range(1, int(noq)+1):
            i = str(q)
            qtype = data['q'+i+'t']

            if qtype == "OBJ":
                qop = []
                qnoo = data.get('q'+i+'noo')
                for o in range(1,int(qnoo)+1):
                    j = str(o)
                    qop.append(data['q'+i+'o'+j])

                ques = {
                            "no": i,
                            "type": "OBJ", 
                            "question": data.get('q'+i+'q'), 
                            "no_of_options": data.get('q'+i+'noo'),
                            "options": qop, 
                            "correct": data.get('q'+i+'co'), 
                            "marks": data.get('q'+i+'marks'),
                            "tag": data.get('q'+i+'tag')
                        }

                allques.append(ques)
                continue

            if qtype == "SUB":
                ques = {
                            "no": i,
                            "type": "SUB", 
                            "question": data.get('q'+i+'q'),
                            "limit": data.get('limit'),
                            "tag": data.get('q'+i+'tag')
                        }

                allques.append(ques)
                continue

            if qtype == "COD":
                ques = {
                            "no": i,
                            "type": "COD", 
                            "question": data.get('q'+i+'q'), 
                            "input": data.get('q'+i+'si'),
                            "output": data.get('q'+i+'so'), 
                            "time_limit": data.get('q'+i+'tl'), 
                            "marks": data.get('q'+i+'marks'),
                            "tag": data.get('q'+i+'tag')
                        }

                allques.append(ques)
                continue

        # saving problem set

        pset['questions'] = allques

        org = OrganizationDB.organization(uno=user['organization'])
        if not org.valid():
            request.session[ADD_PROBLEM_SET_RESULT] = CreatePSetResult.SOMETHING_ELSE.value
            return HttpResponseRedirect("/create/problem-set")

        result, pset = ProblemSetDB.create(pset)

        if not result:
            print("error in creating document in ProblemSets")
            request.session[ADD_PROBLEM_SET_RESULT] = CreatePSetResult.SOMETHING_ELSE.value
            return HttpResponseRedirect("/create/problem-set")

        org['problem_sets'].append(pset['_id'])
        OrganizationDB.update(org)

        request.session[ADD_PROBLEM_SET_RESULT] = CreatePSetResult.ADDED.value
        return HttpResponseRedirect("/create/problem-set")

class CreateTestModule(View):
    def get(self, request):
        context = {}
        if LOGIN_ID not in request.session or LOGIN_TYPE not in request.session:
            return HttpResponseRedirect("/profile")

        if request.session[LOGIN_TYPE] == LoginType.ORG:
            return HttpResponseRedirect("/profile")

        user_id = request.session[LOGIN_ID]
        user_type = request.session[LOGIN_TYPE]

        user = UserDB.user(uno = user_id)
        if not user.valid():
            return HttpResponseRedirect("/profile")

        if user['role'] != TEST_SUPERVISOR:
            return HttpResponseRedirect("/profile")

        user_name_arr = user['name'].split()
        user_init = ""
        for i in user_name_arr:
            user_init += i[0]
        user['initial'] = user_init
        context['user'] = user

        now = datetime.now()

        first_date = now - timedelta(days=now.isoweekday() - 1)

        dates = []
        for count in range(0,21):
            date_entry = {
                            "day": first_date.day, 
                            "date_val": first_date.strftime("%d-%m-%Y"),
                            "date_str": first_date.strftime("%d %B %Y")
                         }
            if first_date > now and first_date <= now + timedelta(days=10):
                date_entry['available'] = True
            else:
                date_entry['available'] = False
            dates.append(date_entry)
            first_date += timedelta(days=1)

        context['dates'] = dates

        if ADD_TEST_MODULE_RESULT in request.session:
            tmcode = request.session[ADD_TEST_MODULE_RESULT]
            context['alert'] = tmcode
            del request.session[ADD_TEST_MODULE_RESULT]

        return render(request, "employee/test-module.html", context)

    def post(self, request):
        
        # validating client
        session = request.session
        if not session.get(LOGIN_ID) or not session.get(LOGIN_TYPE):
            return HttpResponseRedirect("/profile")

        if session[LOGIN_TYPE] == LoginType.ORG:
            return HttpResponseRedirect("/profile")

        user_id = session[LOGIN_ID]
        user_type = session[LOGIN_TYPE]

        user = UserDB.user(uno = user_id)
        if not user.valid():
            return HttpResponseRedirect("/profile")

        if user['role'] != TEST_SUPERVISOR:
            return HttpResponseRedirect("/profile")

        data = request.POST
        test_name = data.get('test_name')
        if not test_name:
            request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.NO_NAME.value
            return HttpResponseRedirect("/create/test-module")

        org = OrganizationDB.organization(uno=user['organization'])
        if not org.valid():
            request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.SOMETHING_ELSE.value
            return HttpResponseRedirect("/create/test-module")

        test_modules = TestModuleDB.all()

        for doc in test_modules:
            if test_name == doc['name'] and user['organization'] == doc['organization']:
                request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.SAME_NAME_EXISTS.value
                return HttpResponseRedirect("/create/test-module")

        if 'no-of-psets' not in data:
            request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.SOMETHING_ELSE.value
            return HttpResponseRedirect("/create/test-module")

        nopset = int(data['no-of-psets'])

        if int(nopset)  <= 0:
            request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.NO_PSET.value
            return HttpResponseRedirect("/create/test-module")

        test_category = data.get('test_category')
        test_description = data.get('test_description')

        test = { 
                    "name": test_name, 
                    "category": test_category,
                    "description": test_description,
                    "organization": org['_id'],
                    "problem_sets": [],
                    "submissions": None,
                    "schedule": None, 
                    "job_offer": None,
                }

        try:
            time_hour = int(str(data.get('time-hour')))
            time_min = int(str(data.get('time-min')))
        except Exception as e:
            print("hello")
            request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.SOMETHING_ELSE.value
            return HttpResponseRedirect("/create/test-module")

        time_am_pm = data.get('time-am-pm')

        if time_am_pm != "PM" and time_am_pm != "AM":
            request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.SOMETHING_ELSE.value
            return HttpResponseRedirect("/create/test-module")

        time_hour -= 1;

        if time_am_pm == "PM":
            time_hour += 12

        time = str(time_hour)+":"+str(time_min)

        schedule = {
                        "date": data.get('date'),
                        "time": time,
                        "duration": data.get('duration')
                    }

        job_offer = {
                        "position": data.get('position'),
                        "type": data.get('type'),
                        "duration": data.get('job-duration'),
                        "salary": data.get('salary'),
                        "currency": data.get('currency'),
                        "description": data.get('job-description')
                    }

        test['schedule'] = schedule
        test['job_offer'] = job_offer

        all_psets = {doc['_id']: doc for doc in ProblemSetDB.all()}

        for i in range(0,nopset):
            pset_id = data.get('ps'+str(i))
            if pset_id:
                test['problem_sets'].append(pset_id)

        result, test = TestModuleDB.create(test)

        if not result:
            print("error in creating document in Test Modules")
            request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.SOMETHING_ELSE.value
            return HttpResponseRedirect("/create/test-module")

        result, subset= SubmissionSetDB.create({"test": test['_id']})
        if result:
            test['submissions'] = subset['_id']
            TestModuleDB.update(test)

        org['test_modules'].append(test['_id'])
        OrganizationDB.update(org)

        request.session[ADD_TEST_MODULE_RESULT] = CreateTMResult.ADDED.value
        return HttpResponseRedirect("/create/test-module")