from django.shortcuts import render
from OnlineRecruitmentSoftware import connection
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

# Create your views here.

def home(request):
	# vcap_config = os.environ.get('VCAP_SERVICES')
	# decoded_config = json.loads(vcap_config)
	# for key in decoded_config.keys():
	# 	if key.startswith('cloudant'):
	# 		cloudant_creds = decoded_config[key][0]['credentials']
	# cloudant_user = str(cloudant_creds['username'])
	# cloudant_pass = str(cloudant_creds['password'])
	# cloudant_url = str(cloudant_creds['url'])
	# cloudant_user = "e65ea042-3f91-4e24-86a1-91719ece201e-bluemix"
	# cloudant_pass = "5ffd728e46615a9aa95c87802b91bf012f83ef0c8a353c0b1bc4adf6b90e886a"
	# cloudant_url = "https://e65ea042-3f91-4e24-86a1-91719ece201e-bluemix:5ffd728e46615a9aa95c87802b91bf012f83ef0c8a353c0b1bc4adf6b90e886a@e65ea042-3f91-4e24-86a1-91719ece201e-bluemix.cloudant.com"
	# #print(cloudant_creds)
	# client = Cloudant(cloudant_user, cloudant_pass, url=cloudant_url, connect=True, auto_renew=True)
	# my_database = client['users']

	context = {"name": ''}
	
	if 'name' in request.session:
		return HttpResponseRedirect("/profile")

	return render(request, "home/home.html", context)

def profile(request):

	context = {"name": '', "is_org": False}
	
	if 'user_id' in request.session:
		client = connection.create()
		
		my_database = None
		if 'user_type' in request.session:
			if request.session['user_type'] == 'O':
				my_database = client['organization']
				context['is_org'] = True
			else:
				my_database = client['users']

		for doc in my_database:
			pass

		user_id = request.session['user_id']

		if user_id in my_database:
			user = my_database[user_id]
			if request.session['user_type'] == 'O':
				context['org'] = user
			else:
				context['user'] = user
				orgs = client['organization']

				for doc in orgs:
					pass

				if 	user['organization'] in orgs:
					org = orgs[user['organization']]
					context['user_org'] = org['name']

			context['user_email'] = user['_id']

			if 'addcode' in request.session:
				add = request.session['addcode']

				if add == 0:
					context['alert'] = 'danger'
					context['alertmessage'] = 'Something Looks Wrong'
				elif add == 1:
					context['alert'] = 'success'
					context['alertmessage'] = 'Added Successfully'
				elif add == 2:
					context['alert'] = 'danger'
					context['alertmessage'] = 'User Does not Exist'
				elif add == 3:
					context['alert'] = 'danger'
					context['alertmessage'] = 'User Already linked to some Organization'

				del request.session['addcode']

			return render(request, "home/profile.html", context)
		else:
			del request.session['user_id']
			del request.session['user_type']
			request.session['authcode'] = 0
			return HttpResponseRedirect("/login?redirect=/profile")

	return HttpResponseRedirect("/login?redirect=/profile")