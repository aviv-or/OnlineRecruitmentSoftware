import json

from django.http import HttpResponse, JsonResponse

from default import LOGIN_ID, LOGIN_TYPE, LoginType, GENERAL_MEMBER
from db.problem_set_database import ProblemSetDB
from db.organization_database import OrganizationDB
from db.user_database import UserDB

def find_problem_sets(request):
    response = {}
    data = request.GET
    session = request.session
    if not session.get(LOGIN_ID) or not session.get(LOGIN_TYPE):
        response['result'] = "error"
        response['message'] = "Login Required"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if session[LOGIN_TYPE] == LoginType.EMP:
        user_id = session[LOGIN_ID]
        user = UserDB.user(uno=user_id)
        if not user.valid():
            response['result'] = "error"
            response['message'] = "Login Required"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

        if user['role'] == GENERAL_MEMBER:
            response['result'] = "error"
            response['message'] = "Permission Not Granted"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)
    
        org = user.organization()

    else:
        org_id = session[LOGIN_ID]
        org = OrganizationDB.organization(uno=org_id)

    s_id = data.get('id')
    s_name = data.get('name')
    s_category = data.get('category')
    s_public = data.get('public')

    s_sort_with = data.get('sort_with')
    s_group_with = data.get('group_with')

    if s_public == "true":
        s_public = True
    else:
        s_public = False

    if s_sort_with != "name" and s_sort_with != "category" and s_sort_with:
        response['result'] = "error"
        response['message'] = "Unknown Sort Type"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if s_group_with != "category" and s_group_with:
        response['result'] = "error"
        response['message'] = "Unknown Group Type"
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
    # print("name = "+str(s_name))
    # print("category = "+str(s_category))
    # print("sort_with = "+str(s_sort_with))
    # print("group_with = "+str(s_group_with))

    if s_id:
        pset = ProblemSetDB.problem_set(uno=s_id)
        if not pset.valid():
            response['result'] = "error"
            response['message'] = "Problem Set Does not exist"
            return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

        response['result'] = "success"
        response['length'] = 1
        response['organization'] = org['_id']
        response['problem_sets'] = [pset]
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if s_public:
        psets = ProblemSetDB.all()
        pset_list = [pset for pset in psets if pset['public'] or pset['organization'] == org['_id']]
    else:
        pset_list = org.problem_sets()

    count, pset_list = problem_sets(pset_list, s_name, s_category, s_from, s_max)

    if s_sort_with:
        pset_list = sort(pset_list, s_sort_with)

    if s_group_with:
        pset_list = group(pset_list, s_group_with)

    if not pset_list or count == 0:
        response['result'] = "success"
        response['length'] = 0
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    for ps in pset_list:
        ps['id'] = ps['_id']
        del ps['_id']
        ps['organization'] = ps.organization()
        ps['organization']['id'] = ps['organization'].get('_id')

    response['result'] = "success"
    response['length'] = count
    response['organization'] = org['_id']
    response['problem_sets'] = pset_list

    return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

def problem_sets (psets, name=None, category=None, s_from=1, s_max=6):
    pset_list = []
    result = []

    if name or category:
        for pset in psets:
            if name and category:
                if pset['name'].lower().startswith(name.lower())\
                and pset['category'].lower().startswith(category.lower()):
                    pset_list.append(pset)
            elif name:
                if pset['name'].lower().startswith(name.lower()):
                    pset_list.append(pset)

            elif category:
                if pset['category'].lower().startswith(category.lower()):
                    pset_list.append(pset)
    else:
        pset_list = psets

    itr_from = 1;
    itr_max = 0;

    for pset in pset_list:
        if itr_from < s_from:
            itr_from = itr_from + 1
            continue
        elif itr_max < s_max:
            itr_max = itr_max + 1
            result.append(pset)
        else:
            break

    return itr_max, result

def sort(psets, key):
    result = sorted(psets, key=lambda pset: pset[key].lower())
    return result

def group(psets, key):
    result = []
    temp = {}
    for pset in psets:
        if pset[key] not in temp:
            temp[pset[key]] = []
        temp[pset[key]].append(pset)

    for pset_group in temp.values():
        result.append(pset_group)

    return result