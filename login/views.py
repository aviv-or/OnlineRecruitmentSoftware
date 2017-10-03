from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import View

# Create your views here.

class LoginHandler(View):
	def get(self,request):
		return render(request, "login.html", {'redirect': request.GET['redirect']});

	def post(self,request):
		pwd = request.POST['pwd']
		email = request.POST['email']
		redirect = request.POST['redirect']
		if email == "d@d.com" and pwd == "1234":
			request.session['name'] = 'shashwat'
			print("session set")
			return HttpResponseRedirect(redirect)
		else:
			return HttpResponseRedirect("/login?redirect="+redirect);

class LogoutHandler(View):
	def get(self,request):
		redirect = request.GET['redirect']
		del request.session['name']
		return HttpResponseRedirect(redirect)
