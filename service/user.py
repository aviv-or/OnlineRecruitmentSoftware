import json

from django.http import JsonResponse

from default import LOGIN_ID, LOGIN_TYPE, LoginType, GENERAL_MEMBER
from db.user_database import UserDB
from db.organization_database import OrganizationDB

def change(request):
    response = {}
    data = request.GET
    session = request.session
    if not session.get(LOGIN_ID) or not session.get(LOGIN_TYPE):
        response['result'] = "error"
        response['message'] = "Login Required"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if session[LOGIN_TYPE] != LoginType.EMP:
        response['result'] = "error"
        response['message'] = "Not a User"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    user_id = session[LOGIN_ID]
    user = UserDB.user(uno=user_id)
    if not user.valid():
        response['result'] = "error"
        response['message'] = "Login Required"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    u_name = data.get('name')
    u_email = data.get('email')
    u_website = data.get('website')
    u_description = data.get('description')

    if ('name' in data and not u_name) or ('email' in data and not u_email):
        response['result'] = "error"
        response['message'] = "No Input"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if u_name:
        user['name'] = u_name

    if u_email:
        user['email'] = u_email

    if 'website' in data:
        user['website'] = u_website

    if 'description' in data:
        user['description'] = u_description

    if not user.valid():
        response['result'] = "error"
        response['message'] = user.error.value
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    result = UserDB.update(user)

    if not result:
        response['result'] = "error"
        response['message'] = "Something Wrong Happened"
        return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)

    if u_name:
        name = user['name']
        name_arr = name.split()
        name = ""
        for i in name_arr:
            name += i[0]
        response['user_initials'] = name

    response['result'] = "success"
    response['message'] = "Changed Successfully"
    return JsonResponse(json.dumps(response, indent=4, sort_keys=True), safe=False)