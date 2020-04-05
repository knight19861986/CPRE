import requests
import configparser
import json

config = configparser.ConfigParser()
config.read('properties.ini')

def get_access_token_by_code(code):
    client_id = config['Tink']['ClientId']
    client_secret = config['Tink']['Client_secret']
    url= 'https://api.tink.com/api/v1/oauth/token'
    grant_type = 'authorization_code'
    data = {'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type
            }
    response = requests.post(url, data=data)
    access_token = response.json()['access_token']
    return access_token

def get_transaction_by_token(access_token):
    url = 'https://api.tink.com/api/v1/transactions'
    hed = {'Authorization': 'Bearer ' + access_token}
    trans = requests.get(url, headers=hed)
    return trans.json()