from cloudant.client import Cloudant
from cloudant.adapters import Replay429Adapter
client = None

def create():

    # vcap_config = os.environ.get('VCAP_SERVICES')
    # decoded_config = json.loads(vcap_config)
    # for key in decoded_config.keys():
    #   if key.startswith('cloudant'):
    #       cloudant_creds = decoded_config[key][0]['credentials']
    # cloudant_user = str(cloudant_creds['username'])
    # cloudant_pass = str(cloudant_creds['password'])
    # cloudant_url = str(cloudant_creds['url'])
    # cloudant_user = "e65ea042-3f91-4e24-86a1-91719ece201e-bluemix"
    # cloudant_pass = "5ffd728e46615a9aa95c87802b91bf012f83ef0c8a353c0b1bc4adf6b90e886a"
    # cloudant_url = "https://e65ea042-3f91-4e24-86a1-91719ece201e-bluemix:5ffd728e46615a9aa95c87802b91bf012f83ef0c8a353c0b1bc4adf6b90e886a@e65ea042-3f91-4e24-86a1-91719ece201e-bluemix.cloudant.com"
    # #print(cloudant_creds)
    # client = Cloudant(cloudant_user, cloudant_pass, url=cloudant_url, connect=True, auto_renew=True)
    # my_database = client['users']

    global client
    if client:
        return client

    cloudant_user = "e65ea042-3f91-4e24-86a1-91719ece201e-bluemix"
    cloudant_pass = "5ffd728e46615a9aa95c87802b91bf012f83ef0c8a353c0b1bc4adf6b90e886a"
    cloudant_url = "https://e65ea042-3f91-4e24-86a1-91719ece201e-bluemix:5ffd728e46615a9aa95c87802b91bf012f83ef0c8a353c0b1bc4adf6b90e886a@e65ea042-3f91-4e24-86a1-91719ece201e-bluemix.cloudant.com"
    client = Cloudant(cloudant_user, cloudant_pass, url=cloudant_url, connect=True, auto_renew=True, adapter=Replay429Adapter(retries=10, initialBackoff=0.01))
    return client