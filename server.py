import configparser
import utils
from flask import Flask, request, render_template, redirect
from werkzeug.urls import iri_to_uri

app = Flask(__name__)
app.debug = True
config = configparser.ConfigParser()
config.read('properties.ini')
#tinkURL= utils.generateTinkLink()
tinkURL= 'https://link.tink.com/1.0/authorize/?client_id=51f92b60022c4b70a29bee5da58aae62&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&scope=accounts:read,transactions:read,user:read&market=SE&locale=en_US'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tinklink')
def tinkLink():
    return redirect(tinkURL)

@app.route('/' + config['Local']['CallBackDir'])
def result():
    tinkCode = request.args.get('code')
    credentialsId = request.args.get('credentialsId')
    return tinkCode + '\n' +credentialsId

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

