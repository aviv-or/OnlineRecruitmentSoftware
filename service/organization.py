import json
from datetime import datetime, date, time

from django.http import HttpResponse, JsonResponse

from db import connection
from db.organization_database import OrganizationDB
from db.user_database import UserDB

from default import LOGIN_ID, LOGIN_TYPE, LoginType
from default import ORGANIZATIONS, TEST_MODULES

def users_data(request):
    if LOGIN_ID not in request.session \
    or LOGIN_TYPE not in request.session:
        return JsonResponse("")

    if request.session[LOGIN_TYPE] != LoginType.ORG \
    or not 'name' in request.GET:
        return JsonResponse("")

    name = request.GET['name']
    name = name.lower()

    if name == "":
        return JsonResponse("")

    org_id = request.session[LOGIN_ID]
    org = OrganizationDB.organization(uno=org_id)
    if not org.valid():
        return JsonResponse("")

    users = UserDB.all()

    josn_string = '{"users_data":['

    nou = 0

    for user in users:
        if user['name'].lower().startswith(name):
            nou += 1
            if nou != 1:
                josn_string += ', '
            josn_string += '{"id":"'+user['_id']+'", "name":"'+user['name']+'", "email":"'+user['email']+'"'
            if user['organization']:
                josn_string += ', "available": false'
            else:
                josn_string += ', "available": true'
            josn_string += '}'

    josn_string += '], "no_of_users":'+str(nou)+'}'

    if nou == 0:
        return JsonResponse("")
    else:
        return JsonResponse(josn_string, safe=False)


def organizations(request):

    data = request.GET
    s_name = None
    if 'name' in data:
        s_name = data['name']

    s_from = 1;
    s_max = 6;

    if 'from' in data:
        s_from = data['from']
        if int(s_from) <= 0:
            return JsonResponse("")

    if 'max' in data:
        s_max = data['max']
        if int(s_max) <= 0:
            return JsonResponse("")

    client = connection.create()
    orgs = client[ORGANIZATIONS]