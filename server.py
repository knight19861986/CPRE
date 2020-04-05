import configparser
from utils import *
from flask import Flask, jsonify, request, render_template, redirect
from werkzeug.urls import iri_to_uri
from requests.models import PreparedRequest

app = Flask(__name__)
app.debug = True
config = configparser.ConfigParser()
config.read('properties.ini')
#tinkURL = 'https://link.tink.com/1.0/authorize/?client_id=51f92b60022c4b70a29bee5da58aae62&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&scope=accounts:read,transactions:read,user:read,identity:read&market=SE&locale=en_US'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tinklink')
def tinkLink():
    req = PreparedRequest()
    redirect_uri = 'http://' + config['Local']['CallBackAddr'] + ':' + config['Local']['CallBackPort'] + '/' + config['Local']['CallBackDir']
    params = {
        'client_id': config['Tink']['ClientId'], 
        'redirect_uri': redirect_uri,
        'market': config['Tink']['Market'], 
        'locale': config['Tink']['Locale']
        }
    req.prepare_url(config['Tink']['BaseUrl'], params)
    scope = "&scope=accounts:read,transactions:read,user:read"
    tinkURL = req.url + scope
    return redirect(tinkURL)

@app.route('/' + config['Local']['CallBackDir'])
def result():
    tinkCode = request.args.get('code')
    #credentialsId = request.args.get('credentialsId')
    access_token = get_access_token_by_code(tinkCode)
    transaction_list = get_transaction_by_token(access_token)
    infected_list = ['Coop']
    #Futrue work: get the infected_list from DB
    user_age = get_user_profile(access_token)
    count = find_in_transaction(transaction_list, infected_list)
    result = assess_result(count, user_age)
    level_dic = {2:"high", 1:"middle", 0:"low"}

    return "You risk of infection is " + level_dic[result]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

