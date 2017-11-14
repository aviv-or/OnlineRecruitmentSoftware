from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from db import connection, authhelper
from db.organization_database import OrganizationDB
from default import ADMIN, ADMIN_ID, AUTH_RESULT, ORGANIZATIONS
from login.error import LoginError

class AdminLogin(View):
	def get(self, request):
		context = {}
		if AUTH_RESULT in request.session:
			if request.session[AUTH_RESULT] == LoginError.SOMETHING_ELSE:
				context["alert"] = { "type": "danger", "message" : "Something looks Wrong" }

			elif request.session[AUTH_RESULT] == LoginError.WRONG_USERNAME_OR_PASSWORD:
				context["alert"] = { "type": "danger", "message" : "Wrong Username or Password" }

			del request.session[AUTH_RESULT]

		return render(request, "admin/login.html", context)

	def post(self, request):
		client = connection.create()
		my_database = client[ADMIN]

		for doc in my_database:
			pass

		if 'email' in request.POST and 'pwd' in request.POST:
			email = request.POST['email']
			pwd = request.POST['pwd']
			if email in my_database:
				doc = my_database[email]
				if doc['password'] == pwd:
					request.session[ADMIN_ID] = doc['_id']
					return HttpResponseRedirect("/admin/profile")

			request.session[AUTH_RESULT] = LoginError.WRONG_USERNAME_OR_PASSWORD
			return HttpResponseRedirect("/admin/login")

		else:
			request.session[AUTH_RESULT] = LoginError.SOMETHING_ELSE
			return HttpResponseRedirect("/admin/login")

class AdminLogout(View):
	def get(self, request):
		if ADMIN_ID in request.session:
			del request.session[ADMIN_ID]

		return HttpResponseRedirect("/")

class AdminProfile(View):
	def get(self, request):
		context = {}
		if ADMIN_ID in request.session:
			admin_id = request.session[ADMIN_ID]
			client = connection.create()
			my_database = client[ADMIN]
			for doc in my_database:
				pass

			if admin_id in my_database:
				admin = my_database[admin_id]
				context['admin_name'] = admin['name']
				orgs = OrganizationDB.all()
				arr = []
				for org in orgs:
					if not org['verified']:
						org['id'] = org['_id']
						arr.append(org)

				context['orgs'] = arr

				return render(request, "admin/profile.html", context)
			else:
				print("no "+admin_id+" in my_database")

			del request.session[ADMIN_ID]
			request.session[AUTH_RESULT] = LoginError.SOMETHING_ELSE
			return HttpResponseRedirect("/admin/login")
		else:
			return HttpResponseRedirect("/")

	def post(self, request):
		return HttpResponseRedirect("/")

class VerifyOrganization(View):
	def get(self, request, org=None):
		if org:
			if ADMIN_ID in request.session:
				admin_id = request.session[ADMIN_ID]
				client = connection.create()
				my_database = client[ADMIN]
				for doc in my_database:
					pass

				if admin_id in my_database:
					org = OrganizationDB.organization(uno=org)
					if not org.valid():
						return HttpResponseRedirect("/admin/profile")
					org['verified'] = True
					OrganizationDB.update(org)

		return HttpResponseRedirect("/admin/profile")