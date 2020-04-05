import requests
import configparser
import json
from datetime import date 

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
    res = requests.get(url, headers=hed)
    transaction = res.json()
    description_list = get_description_list(transaction)
    return description_list

def get_description_list(transaction):
    description_list = []
    for trans in transaction:
        description_list.append(trans['description'])
    return description_list

def find_in_transaction(transaction_list, infected_list):
    count = 0
    for infected_area in infected_list:
        for i in transaction_list:
            if infected_area in i:
                count +=1
    return count

def get_user_profile(access_token):
    url = 'https://api.tink.com/api/v1/user/profile'
    hed = {'Authorization': 'Bearer ' + access_token}
    res = requests.get(url, headers=hed)
    user_birth = res.json()['birth']
    user_age = calculate_age(user_birth)
    return user_age

def calculate_age(birth): 
    today = date.today()
    date_list = birth.split('-')
    for i in range(len(date_list)):
        date_list[i] = int(date_list[i]) 
    age = today.year - date_list[0] - ((today.month, today.day) < (date_list[1], date_list[2])) 
    return age 

def assess_result(count, user_age):
    if count == 1:
        if user_age > 65:
            result = 2
            return result
        result = 1
    elif count > 1:
        result = 2
    else:
        result = 0
    return result
