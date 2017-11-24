import json
from datetime import datetime, date, timedelta

from django.http import HttpResponse, JsonResponse

from db.test_module_database import TestModuleDB
from db.organization_database import OrganizationDB
from db.user_database import UserDB
from db.submission_database import SubmissionDB

from default import LoginType, LOGIN_ID, LOGIN_TYPE

def find_tests (request):
    response = {}
    data = request.GET
    s_id = data.get('id')
    s_name = data.get('name')
    s_category = data.get('category')
    s_test_type = data.get('test_type')
    s_seperate_types = data.get('seperate_types')

    if s_seperate_types == "true":
        s_seperate_types = True
    else:
        s_seperate_types = False

    if not s_test_type:
        s_test_type = "all"
    if s_test_type != "all" and s_test_type != "live" \
    and s_test_type != "upcomming" and s_test_type != "completed":
        response['result'] = "error"
        response['message'] = "Unknown Test Type"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    s_sort_with = data.get('sort_with')
    if s_sort_with != "date" and s_sort_with != "name" \
    and s_sort_with != "category" and s_sort_with:
        response['result'] = "error"
        response['message'] = "Unknown Sort Type"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    s_group_with = data.get('group_with')
    if s_group_with != "organization" and s_group_with != "category"\
    and s_group_with:
        response['result'] = "error"
        response['message'] = "Unknown Group Type"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    org = data.get('organization')
    if org:
        org = OrganizationDB.organization(uno=org)
        if not org.valid():
            response['result'] = "error"
            response['message'] = "not a valid organization"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    try:
        s_from = int(data.get('from',1))
    except Exception as e:
        response['result'] = "error"
        response['message'] = "value of parameter 'from' is not an integer"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    try:
        s_max = int(data.get('max',6))
    except Exception as e:
        response['result'] = "error"
        response['message'] = "value of parameter 'max' is not an integer"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if s_from <= 0:
        response['result'] = "error"
        response['message'] = "value of parameter 'from' is less than 1"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if s_max <= 0:
        response['result'] = "error"
        response['message'] = "value of parameter 'max' is less than 1"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    # print("id = "+str(s_id))
    # print("from = "+str(s_from))
    # print("max = "+str(s_max))
    # print("org = "+str(org))
    # print("name = "+str(s_name))
    # print("category = "+str(s_category))
    # print("sort_with = "+str(s_sort_with))
    # print("group_with = "+str(s_group_with))
    # print("seperate_types = "+str(s_seperate_types))

    if s_id:
        test = TestModuleDB.test_module(uno=s_id)
        if not test.valid():
            response['result'] = "error"
            response['message'] = "Test does not exist"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

        test['pretty_date'] = test.pretty_date()
        test['pretty_duration'] = test.pretty_duration()
        response['result'] = "success"
        response['length'] = 1
        response['tests'] = [test]
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    test_list = []
    if org:
        test_list = org.tests()

    else:
        test_list = TestModuleDB.all()

    if s_sort_with:
        test_list = sort(test_list, s_sort_with)

    count, test_list = tests(test_list, s_name, s_category, s_from, s_max, s_test_type)

    if s_group_with:
        test_list = group(test_list, s_group_with)

    if not test_list or count == 0:
        response['result'] = "success"
        response['length'] = 0
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    for t in test_list:
        t['id'] = t['_id']
        t['pretty_date'] = t.pretty_date()
        t['pretty_duration'] = t.pretty_duration()
        if t.is_live():
            t['status'] = "live"
            t['pretty_remaining_time'] = t.pretty_remaining_time(True)
        elif t.is_completed():
            t['status'] = "completed"
        else:
            t['status'] = "coming"
            t['pretty_remaining_time'] = t.pretty_remaining_time()
        del t['_id']

    response['result'] = "success"
    response['length'] = count
    response['tests'] = test_list

    return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)


def remaining_time(request):
    response = {}
    data = request.GET
    s_id = data.get('id')
    if not s_id:
        response['result'] = "error"
        response['message'] = "No Test Provided"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    s_include = data.get('include')
    if s_include and (s_include != "duration"):
        response['result'] = "error"
        response['message'] = "Unknown Include Type"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    s_pretty = data.get('pretty_time')
    if s_pretty and (s_pretty != "true" or s_pretty != "false"):
        response['result'] = "error"
        response['message'] = "Unknown Pretty Time Value"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    test = TestModuleDB.test_module(uno=s_id)
    if not test.valid(schedule=True):
        response['result'] = "error"
        response['message'] = "Test Doesn't Exists"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if s_pretty == "true":
        response['result'] = "success"
        if s_include:
            response['date'] = test.pretty_remaining_time(include_duration=True)
        else:
            response['date'] = test.pretty_remaining_time()
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)
    else:
        if s_include:
            days, hours, minutes = test.remaining_time(include_duration=True)
        else:
            days, hours, minutes = test.remaining_time()

        response['result'] = "success"
        response['days'] = days
        response['hours'] = hours
        response['minutes'] = minutes
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

def questions(request):
    response = {}
    found_sub = None
    answer = None
    data = request.GET
    test_id = data.get('id')
    pset_id = data.get('category')
    ques_no = data.get('question')
    if not test_id or not pset_id or not ques_no:
        response['result'] = "error"
        response['message'] = "Wrong Data Provided"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    test = TestModuleDB.test_module(uno=test_id)
    if not test.valid():
        response['result'] = "error"
        response['message'] = "Test Doesn't Exist"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    login_id = request.session.get(LOGIN_ID)
    login_type = request.session.get(LOGIN_TYPE)

    if not login_id or not login_type:
        response['result'] = "error"
        response['message'] = "Login Required"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if login_type == LoginType.ORG:
        org = OrganizationDB.organization(uno=login_id)
        if not org.valid():
            response['result'] = "error"
            response['message'] = "Something Looks Wrong with the Login"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    elif login_type == LoginType.EMP:
        user = UserDB.user(uno=login_id)
        if not user.valid():
            response['result'] = "error"
            response['message'] = "Something Looks Wrong with the Login"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

        if not user['role'] or not user['organization']:
            if not test.is_live():
                response['result'] = "error"
                response['message'] = "Test is Not Live"
                return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

            submission = user.submission(test=test_id)
            if submission.valid():
                found_sub = submission

    psets = test.problem_sets()
    if pset_id not in [p['_id'] for p in psets]:
        response['result'] = "error"
        response['message'] = "Category Doesn't Exist"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    pset = {}
    for p in psets:
        if p['_id'] == pset_id:
            pset = p

    questions = pset['questions']
    if len(questions) < int(ques_no) or int(ques_no) < 0:
        response['result'] = "error"
        response['message'] = "Question Doesn't Exist"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    ques = {}
    for q in questions:
        if q['no'] == int(ques_no):
            ques = q

    if ques.get('correct'):
        del ques['correct']
    if ques.get('input'):
        del ques['input']
    if ques.get('output'):
        del ques['output']

    if found_sub:
        answer = found_sub.response(pset_id, ques_no)

    response['result'] = "success"
    response['question'] = ques
    response['submitted_data'] = answer
    return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)


def reviews(request):
    response = {}
    data = request.GET
    s_id = data.get('id')

    if not s_id:
        response['result'] = "error"
        response['message'] = "No Test Provided"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    try:
        s_from = int(data.get('from',1))
    except Exception as e:
        response['result'] = "error"
        response['message'] = "value of parameter 'from' is not an integer"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    try:
        s_max = int(data.get('max',6))
    except Exception as e:
        response['result'] = "error"
        response['message'] = "value of parameter 'max' is not an integer"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if s_from <= 0:
        response['result'] = "error"
        response['message'] = "value of parameter 'from' is less than 1"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if s_max <= 0:
        response['result'] = "error"
        response['message'] = "value of parameter 'max' is less than 1"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    test = TestModuleDB.test_module(uno=s_id)
    if not test.valid():
        response['result'] = "error"
        response['message'] = "Test does not exist"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if not test.is_completed():
        response['result'] = "error"
        response['message'] = "Reviews are visible after the Test is completed"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    itr_from = 1;
    itr_max = 0;
    s_reviews = []

    for review in test.get('reviews').values():
        if itr_from < s_from:
            itr_from = itr_from + 1
            continue
        elif itr_max < s_max:
            itr_max = itr_max + 1
            s_reviews.append(review)
        else:
            break

    response['result'] = "success"
    response['length'] = itr_max
    response['reviews'] = s_reviews
    return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

def save_response(request):
    response = {}
    found_sub = None
    data = request.GET
    session = request.session
    test_id = data.get('id')
    pset_id = data.get('category')
    ques_no = data.get('question')
    answer = data.get('response')
    if not test_id or not pset_id or not ques_no:
        response['result'] = "error"
        response['message'] = "Wrong Data Provided"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if not answer or answer == "":
        answer = None

    test = TestModuleDB.test_module(uno=test_id)
    if not test.valid():
        response['result'] = "error"
        response['message'] = "Test Doesn't Exist"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    login_id = request.session.get(LOGIN_ID)
    login_type = request.session.get(LOGIN_TYPE)

    if not login_id or not login_type:
        response['result'] = "error"
        response['message'] = "Login Required"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if login_type == LoginType.ORG:
        org = OrganizationDB.organization(uno=login_id)
        if not org.valid():
            response['result'] = "error"
            response['message'] = "Something Looks Wrong with the Login"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    elif login_type == LoginType.EMP:
        user = UserDB.user(uno=login_id)
        if not user.valid():
            response['result'] = "error"
            response['message'] = "Something Looks Wrong with the Login"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

        if not user['role'] or not user['organization']:
            if not test.is_live():
                response['result'] = "error"
                response['message'] = "Test is Not Live"
                return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

            submission = user.submission(test=test_id)
            if submission.valid():
                found_sub = submission

    psets = test.problem_sets()
    if pset_id not in [p['_id'] for p in psets]:
        response['result'] = "error"
        response['message'] = "Category Doesn't Exist"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    pset = {}
    for p in psets:
        if p['_id'] == pset_id:
            pset = p

    questions = pset['questions']
    if len(questions) < int(ques_no) or int(ques_no) < 0:
        response['result'] = "error"
        response['message'] = "Question Doesn't Exist"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if found_sub:
        found_sub.save_response(pset_id, ques_no, answer)
        SubmissionDB.update(found_sub)

    response['result'] = "success"
    return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

def save_review(request):
    response = {}
    found_sub = None
    data = request.GET
    session = request.session
    test_id = data.get('id')
    review = data.get('review')

    if not test_id:
        response['result'] = "error"
        response['message'] = "No Test Provided"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    test = TestModuleDB.test_module(uno=test_id)
    if not test.valid():
        response['result'] = "error"
        response['message'] = "Test Doesn't Exist"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    login_id = request.session.get(LOGIN_ID)
    login_type = request.session.get(LOGIN_TYPE)

    if not login_id or not login_type:
        response['result'] = "error"
        response['message'] = "Login Required"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if login_type == LoginType.ORG:
        response['result'] = "error"
        response['message'] = "Only a Participant can Review"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    elif login_type == LoginType.EMP:
        user = UserDB.user(uno=login_id)
        if not user.valid():
            response['result'] = "error"
            response['message'] = "Something Looks Wrong with the Login"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

        if user['role'] or user['organization']:
            response['result'] = "error"
            response['message'] = "Only a Participant can Review"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

        test['review'][user['_id']] = review
        TestModuleDB.update(test)

        response['result'] = "sucess"
        response['message'] = "Review Saved"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

def tests (tests, name=None, category=None, s_from=1, s_max=6, s_type="all"):
    test_list = []
    result = []

    if s_type == "all":
        if name or category:
            for test in tests:
                if name and category:
                    if test['name'].lower().startswith(name.lower())\
                    and test['category'].lower().startswith(category.lower()):
                        test_list.append(test)
                elif name:
                    if test['name'].lower().startswith(name.lower()):
                        test_list.append(test)

                elif category:
                    if test['category'].lower().startswith(category.lower()):
                        test_list.append(test)
        else:
            test_list = tests
    elif s_type == "live":
        for test in tests:
            if test.is_live():
                if name and category:
                    if test['name'].lower().startswith(name.lower())\
                    and test['category'].lower().startswith(category.lower()):
                        test_list.append(test)
                elif name:
                    if test['name'].lower().startswith(name.lower()):
                        test_list.append(test)
                elif category:
                    if test['category'].lower().startswith(category.lower()):
                        test_list.append(test)
                else:
                    test_list.append(test)
    elif s_type == "upcomming":
        for test in tests:
            if not test.is_live() and not test.is_completed():
                if name and category:
                    if test['name'].lower().startswith(name.lower())\
                    and test['category'].lower().startswith(category.lower()):
                        test_list.append(test)
                elif name:
                    if test['name'].lower().startswith(name.lower()):
                        test_list.append(test)
                elif category:
                    if test['category'].lower().startswith(category.lower()):
                        test_list.append(test)
                else:
                    test_list.append(test)
    elif s_type == "completed":
        for test in tests:
            if test.is_completed():
                if name and category:
                    if test['name'].lower().startswith(name.lower())\
                    and test['category'].lower().startswith(category.lower()):
                        test_list.append(test)
                elif name:
                    if test['name'].lower().startswith(name.lower()):
                        test_list.append(test)
                elif category:
                    if test['category'].lower().startswith(category.lower()):
                        test_list.append(test)
                else:
                    test_list.append(test)
    else:
        return 0, []

    itr_from = 1;
    itr_max = 0;

    for test in test_list:
        if itr_from < s_from:
            itr_from = itr_from + 1
            continue
        elif itr_max < s_max:
            itr_max = itr_max + 1
            result.append(test)
        else:
            break

    return itr_max, result

def live_tests (tests, name=None, category=None, s_from=1, s_max=6, live=True):
    test_list = []
    result = []

    for test in tests:
        if (live and test.is_live())\
        or (not live and not test.is_live()):
            if name and category:
                if test['name'].lower().startswith(name.lower())\
                and test['category'].lower().startswith(category.lower()):
                    test_list.append(test)
            elif name:
                if test['name'].lower().startswith(name.lower()):
                    test_list.append(test)
            elif category:
                if test['category'].lower().startswith(category.lower()):
                    test_list.append(test)
            else:
                test_list.append(test)

    itr_from = 1;
    itr_max = 0;

    for test in test_list:
        if itr_from < s_from:
            itr_from = itr_from + 1
            continue
        elif itr_max < s_max:
            itr_max = itr_max + 1
            result.append(test)
        else:
            break

    return itr_max, result

def sort(tests, key):
    if key == 'date':
        result = sorted(tests, key=lambda test: \
            datetime.strptime(test['schedule']['date']+"-"+test['schedule']['time'], "%d-%m-%Y-%H:%M"),\
            reverse=True)
    else:
        result = sorted(tests, key=lambda test: test[key].lower())

    return result

def group(tests, key):
    result = []
    temp = {}
    for test in tests:
        if test[key] not in temp:
            temp[test[key]] = []
        temp[test[key]].append(test)

    for test_group in temp.values():
        result.append(test_group)

    return result

