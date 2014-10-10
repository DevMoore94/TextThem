import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import requests
import urlparse
from flask.ext.sqlalchemy import SQLAlchemy
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



#create app
app = Flask(__name__)

#Setup Stormpath variables
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['STORMPATH_API_KEY_ID'] =  os.environ['STORMPATH_API_KEY_ID']
app.config['STORMPATH_API_KEY_SECRET'] = os.environ['STORMPATH_API_KEY_SECRET']
app.config['STORMPATH_APPLICATION'] = os.environ['STORMPATH_APPLICATION']

app.config['STORMPATH_ENABLE_USERNAME'] = True
app.config['STORMPATH_REQUIRE_USERNAME'] = True


stormpath_manager = StormpathManager(app)

stormpath_manager.login_view = 'login'





def generateMessage():
	error = None
	#Try to open files
	try:
		#Local Variables
		adjective = None
		noun = None
		lineNum = 0;

		#Open the files
		adjfile = open("static/adjectives.txt",'r')
		nounfile = open("static/nouns.txt",'r')

		#Choose a random line in the files.
		adjRan = random.randint(0,689)
		nounRan = random.randint(0, 3719)


		
		#locate the randomly selected lines in the corrosponding file/
		for line in adjfile:
			if(lineNum == adjRan):
				adjective = line
				break;
			lineNum = lineNum + 1
		lineNum = 0 

		for line in nounfile:
			if(lineNum == nounRan):
				noun = line
				break;
			lineNum = lineNum+1	

		#return the selected words	
		return (adjective, noun)
	#catch if there is a problem opening the files	
	except IOError:
		error = "We are experiencing some problems. Sorry for the inconvenience. :("
		print("ERORR:" + e.message)
		return render_template('randomtext.html', error=error)	
#end of generateMessage() function

@app.route('/' ,methods=['GET', 'POST'] )
def index():
	return render_template('index.html')



@app.route('/sendtext' ,methods=['GET', 'POST'] )
@login_required
def send_text():
   
    error = None

    if request.method == 'POST':
		
		if(request.form['number'] == "" or request.form['message'] == ""):
			error = "Please fill in the above fields"
		else:
			number = request.form['number']
			message = request.form['message']
			requests.post(os.environ['BLOWERIO_URL'] + '/messages', data={'to': '+' + number, 'message': message})
	
    
    return render_template('send.html', error=error)		

@app.route('/login' ,methods=['GET', 'POST'] )
def login():
	return render_template('login.html')
	

	



#register a user
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/RandomGenerator' ,methods=['GET', 'POST'] )
def randomgenerator():
	generated = generateMessage()
	adjective =  generated[0]
	noun = generated[1]

	error = None
	if request.method == 'POST':
		
		if(request.form['number'] == "" ):
			error = "Please fill in number for the text and select an adjective and noun"
		else:
			
			number = request.form['number']
			adjective = request.form['adjective'] 
			noun = request.form['noun']
			message =  (adjective + " " + noun)

			#Sends the text message with BLOWER.IO
			requests.post(os.environ['BLOWERIO_URL'] + '/messages', data={'to': '+' + number, 'message': message})

	

	
	return render_template('randomtext.html',error=error, adjective=adjective, noun=noun)



@app.route('/logout')
@login_required
def logout():
    """
    Log out a logged in user.  Then redirect them back to the main page of the
    site.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/about' ,methods=['GET', 'POST'] )
def aboutUs():
	return render_template('aboutus.html')



if __name__ == '__main__':
    app.run(debug=True)
