import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import requests
import urlparse
from flask.ext.sqlalchemy import SQLAlchemy
import random







#create app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  username = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, email, password,username):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.username = username
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)



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
		return render_template('randomtext.html', error=error)	
#end of generateMessage() function



@app.route('/' ,methods=['GET', 'POST'] )
def home_page():
   
    
	
	 
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

	error = None

	if request.method == 'POST':


		user = request.form['username']
		
		if (True):
			error = 'The username or password you have entered is incorrect'
		else:

			return redirect(url_for('home_page'))
			

	return render_template('login.html',error=error)

#register a user
@app.route('/register', methods=['GET', 'POST'])
def register():

	#Check for missing fields
    error = None
    if request.method == 'POST':
        if request.form['username'] == "" and request.form['password'] == "":
                error = 'Please fill in the password field, Username field and email field. Thank you.'

        elif request.form['password'] == "":
                error = 'Please fill in the password field'

        elif request.form['username'] == "":          
                error = 'Please fill in the username field'

        else:
        	#Create a key in redis database
        	r.set(request['username'], request['password'])

    return render_template('register.html', error=error)\


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
			print message

			requests.post(os.environ['BLOWERIO_URL'] + '/messages', data={'to': '+' + number, 'message': message})

	

	
	return render_template('randomtext.html', adjective=adjective, noun=noun)

@app.route('/about' ,methods=['GET', 'POST'] )
def aboutUs():
	return render_template('aboutus.html')



if __name__ == '__main__':
    app.run()
