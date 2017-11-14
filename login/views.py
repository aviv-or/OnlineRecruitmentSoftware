from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View

from default import LoginType, LOGIN_ID, LOGIN_TYPE, AUTH_RESULT
from db import authhelper
from db.user_database import UserDB
from db.organization_database import OrganizationDB
from entities.user import User
from entities.organization import Organization

from result import LoginResult, RegisterResult

class LoginHandler(View):
	def get(self,request):
		profile = request.GET.get('r',"/profile")
		context = {'redirect': profile}
		session = request.session

		if LOGIN_ID in session:
			if LOGIN_TYPE in session:
				return HttpResponseRedirect(profile)
			else:
				del request.session[LOGIN_ID]

		if LOGIN_TYPE in session:
			del session[LOGIN_TYPE]

		if AUTH_RESULT in session:
			alert = session[AUTH_RESULT]
			context['alert'] = alert
			del session[AUTH_RESULT]

		return render(request, "login/login.html", context)

	def post(self,request):

		data = request.POST
		redirect = data.get('r','/profile')
		email = data.get('email')
		pwd = data.get('pwd')

		if not email or not pwd:
			request.session[AUTH_RESULT] = LoginResult.SOMETHING_ELSE
			return HttpResponseRedirect("/login?r="+redirect)

		if data.get('org'):
			org = OrganizationDB.organization(email = email, password = pwd)

			if not org.valid():
				request.session[AUTH_RESULT] = LoginResult.WRONG_USERNAME_OR_PASSWORD.value
				return HttpResponseRedirect("/login?r="+redirect)

			if not org.verified():
				request.session[AUTH_RESULT] = LoginResult.ORGANIZATION_NOT_VERIFIED.value
				return HttpResponseRedirect("/login?r="+redirect)

			request.session[LOGIN_ID] = org['_id']
			request.session[LOGIN_TYPE] = LoginType.ORG
			return HttpResponseRedirect(redirect)

		else:
			user = UserDB.user(email = email, password = pwd)

			if not user.valid():
				request.session[AUTH_RESULT] = LoginResult.WRONG_USERNAME_OR_PASSWORD.value
				return HttpResponseRedirect("/login?r="+redirect)

			request.session[LOGIN_ID] = user['_id']
			request.session[LOGIN_TYPE] = LoginType.EMP
			return HttpResponseRedirect(redirect)

class LogoutHandler(View):
	def get(self,request):
		redirect = '/'
		if "r" in request.GET:
			redirect = request.GET["r"]

		if LOGIN_TYPE in request.session:
			del request.session[LOGIN_TYPE]
		if LOGIN_ID in request.session:
			del request.session[LOGIN_ID]

		return HttpResponseRedirect(redirect)

class RegisterUser(View):
	def get(self,request):
		context = {}
		if AUTH_RESULT in request.session:
			context['alert'] = request.session[AUTH_RESULT]
			
			del request.session[AUTH_RESULT]
		return render(request, "register/registeruser.html", context)

	def post(self, request):
		data = request.POST
		udata = {}
		udata['name'] = data.get('name')
		udata['email'] = data.get('email')
		udata['password'] = data.get('pwd')

		result, user = UserDB.create(udata)
		if result:
			request.session[AUTH_RESULT] = RegisterResult.NONE.value
			return HttpResponseRedirect("/login?r=/profile")				

		elif user.error == User.Error.EMAIL_ALREADY_EXISTS:
			request.session[AUTH_RESULT] = RegisterResult.EMAIL_ALREADY_EXISTS.value
			return HttpResponseRedirect("/register/user")

		request.session[AUTH_RESULT] = RegisterResult.SOMETHING_ELSE.value
		return HttpResponseRedirect("/register/user")

class RegisterOrg(View):
	def get(self,request):
		context = {}
		if AUTH_RESULT in request.session:
			context['alert'] = request.session[AUTH_RESULT]
			del request.session[AUTH_RESULT]
		return render(request, "register/registerorg.html", context)

	def post(self, request):
		data = request.POST
		odata = {}
		odata['name'] = data.get('name')
		odata['email'] = data.get('email')
		odata['password'] = data.get('pwd')
		odata['website'] = data.get('website')
		odata['location'] = data.get('location')
		odata['description'] = data.get('description')
		odata['category'] = data.get('category')

		result, org = OrganizationDB.create(odata)
		print(result)
		print(org)

		if result:
			request.session[AUTH_RESULT] = RegisterResult.NONE.value
			return HttpResponseRedirect("/login?r=/profile")

		elif org.error == Organization.Error.EMAIL_ALREADY_EXISTS:
			request.session[AUTH_RESULT] = RegisterResult.EMAIL_ALREADY_EXISTS.value
			return HttpResponseRedirect("/register/organization")

		request.session[AUTH_RESULT] = RegisterResult.SOMETHING_ELSE.value
		return HttpResponseRedirect("/register/organization")