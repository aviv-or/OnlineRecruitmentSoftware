from django.shortcuts import render

# Create your views here.

def home(request):
	if 'name' in request.session:
		name = request.session['name']
	else:
		name = ''
	return render(request, "home.html", {'name': name})