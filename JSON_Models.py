
"""
Copyright 2021 Eggplant

Retrieve JSON models from DAI

"""

# Pre-requisites: 
# * PYTHON 3 installed 
# * gitpython installed (e.g. pip install gitpython)

from datetime import date
import requests
import json
import git
import subprocess


with open(r'/Users/pmerrill/Documents/ABSA Work/config.json') as jsonFile:
    config_data = json.load(jsonFile)

username = config_data["username"]
password = config_data["password"]
DAI_server = config_data["DAI_server"]
model_ids = config_data["model_ids"]
auth_url = DAI_server + "/ai/auth"
model_url = DAI_server + "/#/model/"
models_url = DAI_server + "/ai/models/"



def get_token():
    print("************************ Retrieving access token ************************")
    payload = {'username': username, 'password': password}
    AuthResponse = requests.post(auth_url, data=payload)
    ResponseData = AuthResponse.json()
    access_token = ResponseData["access_token"]
    return access_token


# ---------------------------------------------
def request_endpoint(access_token, endpoint):
    headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' + access_token
    }
    request_response = requests.get(endpoint, params={}, headers=headers)
    
    print(request_response)
    return request_response
    # return request_response.json()

# -------------------------------------------------------------

def get_specific_json_models(access_token, models_url, model_ids):
    headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' + access_token
    }    
    
    model_data = []
    for model_id in model_ids:
        model_url_specific = models_url + str(model_id)
        model_details = requests.get(model_url_specific, headers = headers)
        print(model_details.json())

        model_data.append(model_details.json())
    
    print("************************ JSON MODELS RETRIEVED ************************")
    print(model_data)
    
    with open('/Users/pmerrill/Documents/ABSA Work/critical_models.json', 'w') as outfile:
        json.dump(model_data, outfile)
        print("************************ MODELS SENT TO FILE ************************")


# -------------------------------------------------------------

def get_all_json_models(models_url, access_token):
    headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer ' + access_token
    }
    request_response = requests.get(models_url, params={}, headers=headers)
    
    print(request_response)
    print(request_response.json())

    model_data = []
    model_data.append(request_response.json())

    with open('/Users/pmerrill/Documents/ABSA Work/models.json', 'w') as outfile:
        json.dump(model_data, outfile)

# -------------------------------------------------------------

def git_commands():
    my_repo = git.Repo('existing_repo')
    # # Check out via HTTPS
    # git.Repo.clone_from('https://github.com/DevDungeon/Cookbook', 'Cookbook-https')
    # # or clone via ssh (will use default keys)
    # git.Repo.clone_from('git@github.cim:DevDungeon/Cookbook', 'Cookbook-ssh')


    # Provide a list of the files to stage
    my_repo.index.add(['/Users/pmerrill/Documents/ABSA Work/models.json', '/Users/pmerrill/Documents/ABSA Work/critical_models.json'])
    # Provide a commit message
    today = date.today()
    date_formatted = today.strftime("%d/%m/%Y")
    my_repo.index.commit('Adding JSON representations of DAI models ' + str(date_formatted))

    subprocess.call(['sh', './test.sh'])


# -------------------------------------------------------------
access_token = get_token()
print("ACCESS TOKEN: ")
print(access_token)

# get_all_json_models(models_url, access_token)

get_specific_json_models(access_token, models_url, model_ids)


