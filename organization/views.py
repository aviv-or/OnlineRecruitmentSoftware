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

problem_set_code
0: something wrong
1: no questions in problem set
2: no name for problem set
3: problem set with same name exists
4: success
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

		if 'problem_set_code' in request.session:
			pscode = request.session['problem_set_code']

			if pscode == 0:
				context['alert'] = 'danger'
				context['alertmessage'] = 'Something Looks Wrong'

			elif pscode == 1:
				context['alert'] = 'warning'
				context['alertmessage'] = 'No Questions Added'

			elif pscode == 2:
				context['alert'] = 'warning'
				context['alertmessage'] = 'No Name specified for the problem set'

			elif pscode == 3:
				context['alert'] = 'warning'
				context['alertmessage'] = 'Problem Set with this name already exists'

			elif pscode == 4:
				context['alert'] = 'success'
				context['alertmessage'] = 'Added Sucessfully'

			del request.session['problem_set_code']

		return render(request, "organization/create_problem_set.html", context)

	def post(self, request):
		
		# validating client

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

		# validating request

		data = request.POST

		if 'noq' not in data:
			request.session['problem_set_code'] = 0
			return HttpResponseRedirect("/organization/create-problem-set")

		noq = data['noq']

		if int(noq)  <= 0:
			request.session['problem_set_code'] = 1
			return HttpResponseRedirect("/organization/create-problem-set")

		ps_name = data['ps_name']
		if not ps_name:
			request.session['problem_set_code'] = 2
			return HttpResponseRedirect("/organization/create-problem-set")


		pset = {"_id": ps_name, "organisation": user['organization'], "questions": []}
		problem_sets = client['problem_sets']

		for doc in problem_sets:
			pass

		if ps_name in problem_sets:
			request.session['problem_set_code'] = 3
			return HttpResponseRedirect("/organization/create-problem-set")

		allques = []

		for q in range(1, int(noq)+1):
			i = str(q)
			qtype = data['q'+i+'t']
			print("checking type"+qtype)

			if qtype == "OBJ":
				qq = data['q'+i+'q']
				qnoo = data['q'+i+'noo']
				qop = []
				for o in range(1,int(qnoo)+1):
					j = str(o)
					qop.append(data['q'+i+'o'+j])
				qco = data['q'+i+'co']
				qmarks = data['q'+i+'marks']

				ques = {"type": "OBJ", "question": qq, "no_of_options": qnoo, "options": qop, "correct_option": qco, "marks": qmarks}
				qtag = data['q'+i+'tag']
				if qtag:
					ques['tag'] = qtag

				print(ques)
				allques.append(ques)
				continue

			if qtype == "SUB":
				qq = data['q'+i+'q']
				ques = {"type": "SUB", "question": qq}

				if 'q'+i+'tag' in data:
					ques['tag'] = data['q'+i+'tag']

				print(ques)
				allques.append(ques)
				continue

			if qtype == "COD":
				qq = data['q'+i+'q']

				qsi = ''
				if 'q'+i+'si' in data:
					qsi = data['q'+i+'si']

				qso = data['q'+i+'so']
				qtl = data['q'+i+'tl']
				qmarks = data['q'+i+'marks']

				ques = {"type" : "COD", "question" : qq, "input": qsi, "output": qso, "time_limit": qtl, "marks": qmarks }
				qtag = data['q'+i+'tag']
				if qtag:
					ques['tag'] = qtag

				print(ques)
				allques.append(ques)
				continue

		# saving problem set

		pset['questions'] = allques
		
		doc = problem_sets.create_document(pset)

		if not doc.exists():
			print("error in creating document")
			request.session['problem_set_code'] = 0
			return HttpResponseRedirect("/organization/create-problem-set")

		request.session['problem_set_code'] = 4
		return HttpResponseRedirect("/organization/create-problem-set")




