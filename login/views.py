from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View
from OnlineRecruitmentSoftware import connection

# Create your views here.

class LoginHandler(View):
	def get(self,request):
		context = {}
		if 'redirect' in request.GET:
			context["redirect"] = request.GET['redirect']
		else:
			context["redirect"] = '/profile'

		if 'autherror' in request.GET:
			if request.GET["autherror"] == 'true':
				context["error"] = True
			else:
				context["error"] = False
		else:
			context["error"] = False

		return render(request, "login.html", context);

	def post(self,request):
		pwd = request.POST['pwd']
		email = request.POST['email']
		redirect = request.POST['redirect']

		my_database = connection.conn['users']

		if email in my_database:
			doc = my_database[email]
			if doc['password'] == pwd:
				request.session['name'] = doc['name']
				return HttpResponseRedirect(redirect)

		return HttpResponseRedirect("/login?redirect="+redirect+"&&autherror=true")

class LogoutHandler(View):
	def get(self,request):
		redirect = request.GET['redirect']
		del request.session['name']
		return HttpResponseRedirect(redirect)
