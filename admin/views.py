from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from OnlineRecruitmentSoftware import connection, authhelper

# Create your views here.

class AdminLogin(View):
	def get(self, request):
		context = {}
		if 'authcode' in request.session:
			if request.session["authcode"] == 0:
				context['alert'] = 'danger'
				context["alertmessage"] = "Something looks Wrong"

			elif request.session["authcode"] == 1:
				context['alert'] = 'danger'
				context["alertmessage"] = "Wrong Username or Password"

			elif request.session["authcode"] == 2:
				context['alert'] = 'success'
				context["alertmessage"] = "Registration was successful! Log In to Continue"
			
			del request.session['authcode']
		else:
			context["alert"] = False
		return render(request, "admin/login.html", context)

	def post(self, request):
		client = connection.create()
		my_database = client['admin']

		for doc in my_database:
			pass

		if 'email' in request.POST and 'pwd' in request.POST:
			email = request.POST['email']
			pwd = request.POST['pwd']
			if email in my_database:
				doc = my_database[email]
				if doc['password'] == pwd:
					request.session['admin_id'] = doc['_id']
					return HttpResponseRedirect("/admin/profile")

			request.session["authcode"] = 1
			return HttpResponseRedirect("/admin/login")

		else:
			request.session["authcode"] = 0
			return HttpResponseRedirect("/admin/login")

class AdminLogout(View):
	def get(self, request):
		if 'admin_id' in request.session:
			del request.session['admin_id']
			
		return HttpResponseRedirect("/")

class AdminProfile(View):
	def get(self, request):
		context = {}
		if 'admin_id' in request.session:
			admin_id = request.session['admin_id']
			client = connection.create()
			my_database = client['admin']
			for doc in my_database:
				pass

			if admin_id in my_database:
				admin = my_database[admin_id]
				context['admin_name'] = admin['name']
				client2 = connection.create()
				orgs = client2['organization']

				for doc in orgs:
					pass

				arr = []
				for key in orgs.keys():
					o = orgs[key]
					if not o['verified']:
						newd = {}
						newd['name'] = o['name']
						newd['desc'] = o['description']
						newd['email'] = o['_id']
						newd['website'] = o['website']
						newd['location'] = o['location']
						arr.append(newd)

				context['orgs'] = arr

				return render(request, "admin/profile.html", context)
			else:
				print("no "+admin_id+" in my_database")

			del request.session['admin_id']
			request.session["authcode"] = 0
			return HttpResponseRedirect("/admin/login")
		else:
			return HttpResponseRedirect("/")

	def post(self, request):
		return HttpResponseRedirect("/")

class VerifyOrganization(View):
	def get(self, request, org=None):
		if org:
			if 'admin_id' in request.session:
				admin_id = request.session['admin_id']
				client = connection.create()
				my_database = client['admin']
				for doc in my_database:
					pass

				if admin_id in my_database:
					client = connection.create()
					orgs = client['organization']

					for doc in orgs:
						pass

					if org in orgs:
						doc = orgs[org]
						if not doc['verified']:
							doc['verified'] = True
							doc.save()

		return HttpResponseRedirect("/admin/profile")