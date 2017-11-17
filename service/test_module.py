import json
from datetime import datetime, date, timedelta

from django.http import HttpResponse, JsonResponse

from db.test_module_database import TestModuleDB
from db.organization_database import OrganizationDB
import testhelper

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

        response['result'] = "success"
        response['length'] = 1
        response['tests'] = [test]
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    test_list = []
    if org:
        test_list = org.tests()

    else:
        test_list = TestModuleDB.all()

    count, test_list = tests(test_list, s_name, s_category, s_from, s_max, s_test_type)

    if s_sort_with:
        if s_sort_with == "date":
            if s_test_type == "live":
                test_list = sort(test_list, s_sort_with)
        else:
            test_list = sort(test_list, s_sort_with)

    if s_group_with:
        test_list = group(test_list, s_group_with)

    if not test_list or count == 0:
        response['result'] = "success"
        response['length'] = 0
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

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

    test = TestModuleDB.test_module(uno=s_id)
    if not test.valid(schedule=True):
        response['result'] = "error"
        response['message'] = "Test Doesn't Exists"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    days, hours, minutes = testhelper.remaining_time(test)

    response['result'] = "success"
    response['days'] = days
    response['hours'] = hours
    response['minutes'] = minutes
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
            if testhelper.is_live_test(test):
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
            if not testhelper.is_live_test(test)\
            and not testhelper.is_completed_test(test):
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
            if testhelper.is_completed_test(test):
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
        if (live and testhelper.is_live_test(test))\
        or (not live and not testhelper.is_live_test(test)):
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

