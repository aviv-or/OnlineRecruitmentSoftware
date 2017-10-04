from django.shortcuts import render
from OnlineRecruitmentSoftware import connection

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

	context = {}
	
	if 'name' in request.session:
		context['name'] = request.session['name']
	else:
		context['name'] = ''
	return render(request, "home.html", context)