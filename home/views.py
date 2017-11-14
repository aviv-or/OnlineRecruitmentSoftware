from django.shortcuts import render
from OnlineRecruitmentSoftware import connection
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from db.user_database import UserDB
from db.organization_database import OrganizationDB

from db.interface.organization_data import OrganizationData

from default import LOGIN_ID, LOGIN_TYPE, LoginType, AUTH_RESULT
from default import ADD_EMP_RESULT, REMOVE_EMP_RESULT
from result import LoginResult, AddResult, RemoveResult

def home(request):
	session = request.session

	if LOGIN_ID in session and LOGIN_TYPE in session:
		return HttpResponseRedirect("/profile")

	return render(request, "home/home.html", {})

def profile(request):

	context = {}
	
	session = request.session

	if not session.get(LOGIN_ID) or not session.get(LOGIN_TYPE):
		return HttpResponseRedirect("/login?r=/profile")

	user_id = session[LOGIN_ID]
	user_type = session[LOGIN_TYPE]

	if user_type == LoginType.ORG:
		org = OrganizationDB.organization(uno = user_id)

		if not org.valid():
			session[AUTH_RESULT] = LoginResult.SOMETHING_ELSE.value
			return HttpResponseRedirect("/login?r=/profile")

		add_result = session.get(ADD_EMP_RESULT)
		remove_result = session.get(REMOVE_EMP_RESULT)
		if add_result:
			context['alert'] = add_result

			del request.session[ADD_EMP_RESULT]

		elif remove_result:
			context['alert'] = remove_result

			del request.session[REMOVE_EMP_RESULT]

		employees  = {}

		user = org.employees(OrganizationData.EmpType.HR)
		if user.valid():
			user['id'] = user['_id']
			employees[OrganizationData.EmpType.HR.name] = user

		user = org.employees(OrganizationData.EmpType.SU)
		if user.valid():
			user['id'] = user['_id']
			employees[OrganizationData.EmpType.SU.name] = user

		user = org.employees(OrganizationData.EmpType.PS)
		if user.valid():
			user['id'] = user['_id']
			employees[OrganizationData.EmpType.PS.name] = user

		user = org.employees(OrganizationData.EmpType.GN)
		for u in user:
			if u.valid():
				u['id'] = u['_id']
		employees[OrganizationData.EmpType.GN.name] = user

		org['employees'] = employees

		context['org'] = org

		return render(request, "home/orgprofile.html", context)

	else:
		user = UserDB.user(uno = user_id)

		if not user.valid():
			session[AUTH_RESULT] = LoginResult.SOMETHING_ELSE.value
			return HttpResponseRedirect("/login?r=/profile")

		org = user.organization()
		if org.valid():
			user['organization'] = org

		user_name_arr = user['name'].split()
		user_init = ""
		for i in user_name_arr:
			user_init += i[0]
		user['initial'] = user_init
		context['user'] = user

		return render(request, "home/userprofile.html", context)