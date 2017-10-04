from cloudant.client import Cloudant

conn = None

def initialise():
	global conn
	cloudant_user = "e65ea042-3f91-4e24-86a1-91719ece201e-bluemix"
	cloudant_pass = "5ffd728e46615a9aa95c87802b91bf012f83ef0c8a353c0b1bc4adf6b90e886a"
	cloudant_url = "https://e65ea042-3f91-4e24-86a1-91719ece201e-bluemix:5ffd728e46615a9aa95c87802b91bf012f83ef0c8a353c0b1bc4adf6b90e886a@e65ea042-3f91-4e24-86a1-91719ece201e-bluemix.cloudant.com"
	conn = Cloudant(cloudant_user, cloudant_pass, url=cloudant_url, connect=True, auto_renew=True)

def close():
	conn.close()