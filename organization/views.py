from enum import Enum

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View

from db import authhelper
from db.organization_database import OrganizationDB
from db.user_database import UserDB

from entities.user import User
from entities.organization import Organization

from result import AddResult, RemoveResult
from default import AUTH_RESULT, LOGIN_ID, LOGIN_TYPE, LoginType
from default import ADD_EMP_RESULT, REMOVE_EMP_RESULT
from default import GENERAL_MEMBER, TEST_SUPERVISOR, HR_MANAGER, PROBLEM_SETTER
from result import LoginResult

class AddEmployee(View):
	def get(self,request, user=None):
		session = request.session
		if not session.get(LOGIN_ID) or not session.get(LOGIN_TYPE):
			request.session[ADD_EMP_RESULT] = AddResult.SOMETHING_ELSE.value
			return HttpResponseRedirect("/profile")

		if session.get(LOGIN_TYPE) != LoginType.ORG or not user:
			request.session[ADD_EMP_RESULT] = AddResult.SOMETHING_ELSE.value
			return HttpResponseRedirect("/profile")

		org_id = request.session[LOGIN_ID]
		org = OrganizationDB.organization(uno=org_id)
		if not org.valid():
			request.session[AUTH_RESULT] = LoginResult.SOMETHING_ELSE.value
			del request.session[LOGIN_ID]
			del request.session[LOGIN_TYPE]
			return HttpResponseRedirect("/profile")

		if 'mod' not in request.GET:
			request.session[ADD_EMP_RESULT] = AddResult.SOMETHING_ELSE.value
			return HttpResponseRedirect("/profile")

		mod = request.GET['mod']
		user = UserDB.user(uno=user)

		if not user.valid():
			request.session[ADD_EMP_RESULT] = AddResult.EMP_NOT_VALID.value
			return HttpResponseRedirect("/profile")

		if mod == "GN":
			if user.get('organization'):
				request.session[ADD_EMP_RESULT] = AddResult.EMP_NOT_FREE.value
				return HttpResponseRedirect("/profile")

			user['organization'] = org_id
			user['role'] = 'GN'
			org.add(user['_id'])

		else:
			if user['organization'] != org['_id'] \
			or user['role'] != "GN":
				request.session[ADD_EMP_RESULT] = AddResult.EMP_NOT_FREE.value
				return HttpResponseRedirect("/profile")

			if mod == "HR":
				org.set_emp(Organization.EmpType.HR, user['_id'])
				user['role'] = "HR"
			elif mod == "SU":
				org.set_emp(Organization.EmpType.SU, user['_id'])
				user['role'] = "SU"
			elif mod == "PS":
				org.set_emp(Organization.EmpType.PS, user['_id'])
				user['role'] = "PS"
			else:
				request.session[ADD_EMP_RESULT] = AddResult.SOMETHING_ELSE.value
				return HttpResponseRedirect("/profile")

		UserDB.update(user)
		OrganizationDB.update(org)

		request.session[ADD_EMP_RESULT] = AddResult.ADDED.value
		return HttpResponseRedirect("/profile")

class RemoveEmployee(View):
	def get(self,request, user=None):
		if LOGIN_ID not in request.session \
		or LOGIN_TYPE not in request.session:
			request.session[ADD_EMP_RESULT] = RemoveResult.SOMETHING_ELSE.value
			return HttpResponseRedirect("/profile")

		if request.session[LOGIN_TYPE] != LoginType.ORG \
		or not user:
			request.session[ADD_EMP_RESULT] = RemoveResult.SOMETHING_ELSE.value
			return HttpResponseRedirect("/profile")

		org_id = request.session[LOGIN_ID]
		org = OrganizationDB.organization(uno=org_id)
		if not org.valid():
			request.session[AUTH_RESULT] = LoginResult.SOMETHING_ELSE.value
			del request.session[LOGIN_ID]
			del request.session[LOGIN_TYPE]
			return HttpResponseRedirect("/profile")

		user = UserDB.user(uno=user)
		print("1")

		if not user.valid():
			print("1")
			request.session[ADD_EMP_RESULT] = RemoveResult.EMP_NOT_VALID.value
			return HttpResponseRedirect("/profile")

		if user['organization'] != org['_id']:
			print("1")
			request.session[AUTH_RESULT] = RemoveResult.SOMETHING_ELSE.value
			del request.session[LOGIN_ID]
			del request.session[LOGIN_TYPE]
			return HttpResponseRedirect("/profile")

		if user['role'] == "GN":
			org.remove(user['_id'])
			user['role'] = None
			user['organization'] = None

		else:
			if user['role'] == "HR":
				org.remove_emp(Organization.EmpType.HR)
				org.add(user['_id'])
				user['role'] = "GN"
			elif user['role'] == "SU":
				org.remove_emp(Organization.EmpType.SU)
				org.add(user['_id'])
				user['role'] = "GN"
			elif user['role'] == "PS":
				org.remove_emp(Organization.EmpType.PS)
				org.add(user['_id'])
				user['role'] = "GN"
			else:
				print("1")
				request.session[ADD_EMP_RESULT] = RemoveResult.SOMETHING_ELSE.value
				return HttpResponseRedirect("/profile")

		UserDB.update(user)
		OrganizationDB.update(org)

		request.session[ADD_EMP_RESULT] = RemoveResult.REMOVED.value
		return HttpResponseRedirect("/profile")
