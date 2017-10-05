from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from OnlineRecruitmentSoftware import connection, authhelper

# Create your views here.

"""
addcodes:
0: something wrong
1: sucess
2: emp_email not valid
3: emp not free
"""

def add_employee(request):
	if request.method != 'POST' or 'user_id' not in request.session or 'user_type' not in request.session:
		request.session['addcode'] = 0
		return HttpResponseRedirect("/profile")

	if request.session['user_type'] == 'U':
		request.session['addcode'] = 0
		return HttpResponseRedirect("/profile")

	if 'emp_type' in request.POST and 'emp_email' in request.POST:
		emp_type = request.POST['emp_type']
		emp_email = request.POST['emp_email']

		user_id = request.session['user_id']

		client = connection.create()

		# check if organization exists

		orgs = client['organization']

		for doc in orgs:
			pass

		if user_id not in orgs:
			request.session['authcode'] = 0
			del request.session['user_id']
			del request.session['user_type']
			return HttpResponseRedirect("/profile")

		org = orgs[user_id]

		# check if employee to add exists 

		users = client['users']

		for doc in users:
			pass

		if emp_email not in users:
			request.session['addcode'] = 2
			return HttpResponseRedirect("/profile")

		user = users[emp_email]

		# check if user is not assigned to an organization

		if user['organization']:
			request.session['addcode'] = 3
			return HttpResponseRedirect("/profile")

		# save user as an employee

		user['organization'] = org['_id']
		user['role'] = emp_type

		if emp_type == 'GN':
			org['GN'].append(user['_id'])
		else:
			org[emp_type] = user['_id']

		user.save()
		org.save()

		request.session['addcode'] = 1
		return HttpResponseRedirect("/profile")

class CreateProblemSet(View):
	def get(self, request):
		context = {}
		if 'user_id' not in request.session or 'user_type' not in request.session:
			return HttpResponseRedirect("/profile")

		if request.session['user_type'] == 'O':
			return HttpResponseRedirect("/profile")

		user_id = request.session['user_id']
		user_type = request.session['user_type']

		client = connection.create()

		users = client['users']

		for doc in users:
			pass

		if user_id not in users:
			return HttpResponseRedirect("/profile")

		user = users[user_id]

		if user['role'] != 'PS':
			return HttpResponseRedirect("/profile")

		context['user'] = user

		return render(request, "organization/create_problem_set.html", context)