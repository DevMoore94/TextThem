import os, sys
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify, abort
from contextlib import closing
import requests
import urlparse
import redis

import random
from flask.ext.stormpath import (
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)

from stormpath.error import Error as StormpathError

app = Flask(__name__)

if "HEROKU" in os.environ:
    Production = True
else:
    app.config['DEBUG'] = True
    Production = False

#Setup Stormpath variables and Redis DB
if Production:
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['STORMPATH_API_KEY_ID'] = os.environ['STORMPATH_API_KEY_ID']
    app.config['STORMPATH_API_KEY_SECRET'] = os.environ['STORMPATH_API_KEY_SECRET']
    app.config['STORMPATH_APPLICATION'] = os.environ['STORMPATH_APPLICATION']

    url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost'))
    redis = redis.Redis(host=url.hostname, port=url.port, db=0, password=url.password)

else:
    app.config['SECRET_KEY'] = "1s2b3c4dzxy"
    app.config['STORMPATH_API_KEY_ID'] = "C1F8HU66CJ64TAY0138WHEJJX"
    app.config['STORMPATH_API_KEY_SECRET'] = "xLPo62taHnzfhEmGGM0d5hfNpsiQqbx2F/bMeyoS5iM"
    app.config['STORMPATH_APPLICATION'] = "TextThem"

    url = urlparse.urlparse("redis://redistogo:8bc0a4a78f077cca60c78cca6e5a8f1e@dab.redistogo.com:9082/")
    redis = redis.Redis(host=url.hostname, port=url.port, db=0, password=url.password)

app.config['STORMPATH_ENABLE_USERNAME'] = True
app.config['STORMPATH_REQUIRE_USERNAME'] = True
app.config['STORMPATH_ENABLE_FORGOT_PASSWORD'] = True
app.config['STORMPATH_REGISTRATION_TEMPLATE'] = 'register.html'
app.config['STORMPATH_LOGIN_TEMPLATE'] = 'login.html'
app.config['STORMPATH_FORGOT_PASSWORD_TEMPLATE'] = 'forgot.html'
app.config['STORMPATH_FORGOT_PASSWORD_EMAIL_SENT_TEMPLATE'] = 'forgot_email_sent.html'
app.config['STORMPATH_FORGOT_PASSWORD_CHANGE_TEMPLATE'] = 'forgot_change.html'
app.config['STORMPATH_FORGOT_PASSWORD_COMPLETE_TEMPLATE'] = 'forgot_complete.html'

stormpath_manager = StormpathManager(app)
stormpath_manager.login_view = 'login'

#Store messages in redis database.
def logMessage(number, message):
    try:
        redis.rpush(user.username + "_Messages", number + " " + message)
        print("LOGGED")
    except Exception as e:
        print(e.message)

def generateMessage():
    """Generate a random adjective and noun

    Returns:
        tuple - (string, string) - (adjective, noun)
    """

    with open("static/adjectives.txt") as f:
        adjectives = f.readlines()

    with open("static/nouns.txt") as f:
        nouns = f.readlines()

    adjective = random.choice(adjectives).strip()
    noun = random.choice(nouns).strip()

    return (adjective, noun)

@app.route('/smsapi', methods=['GET', 'POST'])
def send_message(data=None):
    """function for sending sms.
        validates if user is valid > sends message > redirects to source path
        Assumes URL of the form /smsapi?number=12341234&message=message&source=/url
    """
    number = request.args.get('number')
    message = request.args.get('message')
    source = request.args.get('source', '/')
    anonymous = request.args.get('anonymous')

    if message is not None:
        if len(message) > 141:
            abort(400)
    
    if number is None:
        abort(400)

    if(anonymous==None):
        logMessage(number,message)

    if Production:
        requests.post(os.environ['BLOWERIO_URL'] + '/messages', data={'to': '+' + number, 'message': message})
    else:      
        app.logger.info(str({'to': '+' + number, 'message': message}))

         
        

    return  redirect("."+source)


@app.route('/', methods=['GET', 'POST'])
def index():

    contacts = [] if user.is_anonymous() else redis.lrange(user.username +"_phonebook",0,-1)

    if(user.is_anonymous()):
        messages = []
    else:
        messages = redis.lrange(user.username +"_Messages",0,-1)
            
    return render_template('index.html', contacts=contacts, messages=reversed(messages))


@app.route('/sendtext', methods=['GET', 'POST'])
def send_text():
    
    anonymous = None
    error = None

    if(user.is_anonymous()):
        contacts = []
    else:
        contacts = redis.lrange(user.username +"_phonebook",0,-1)
    
    
    if request.method == 'POST':

        if 'Anonymous_checkbox' in request.form:
           anonymous = True
      

        if (request.form['number'] == "" or request.form['message'] == ""):
            error = "Please fill in the above fields"
        else:
            number = request.form['number']
            message = request.form['message']
            return redirect(url_for('send_message', number=number, message=message,anonymous=anonymous, source = "/sendtext"))


    return render_template('send.html', error=error, contacts=contacts)


@app.route('/login', methods=['GET', 'POST'])
def login():

    return render_template('login.html')

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    

    if request.method == 'POST':
        
        redis.rpush(user.username+"_phonebook", request.form['contact_name'] +" - " + request.form['contact_number'] )

    return render_template('manage.html')

#register a user
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/RandomGenerator', methods=['GET', 'POST'])
def randomgenerator():
    generated = generateMessage()
    return(jsonify(noun=generated[0], adjective=generated[1]))

@app.route('/ClearHistory', methods=['GET', 'POST'])
def clearhistory():
    redis.delete(user.username + "_Messages")
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/about', methods=['GET', 'POST'])
def aboutUs():
    return render_template('aboutus.html')

if __name__ == "__main__":
    app.run()
