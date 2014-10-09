import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import requests
import urlparse
from flask.ext.sqlalchemy import SQLAlchemy
import random
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID




#path to tmp folder for openID
#basedir = os.path.abspath(os.path.dirname(__file__))



#create app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://xqogpkihzswsuo:GHLg4AsJTF7rgyJv5fa3hj3dxI@ec2-184-73-194-196.compute-1.amazonaws.com:5432/d5a4164ud0gk36"
db = SQLAlchemy(app)


#setups flask-login
try:
	lm = LoginManager()
	lm.init_app(app)
#oid = OpenID(app,'static/tmp')
except Exception as e:
	print "ERROR: " + e.message

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  username = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, username, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.username = username
    self.email = email.lower()
    self.password = password
  

  def is_authenticated(self):
  	return True

  def is_active(self):
        return True

  def is_anonymous(self):
        return False

  def get_id(self):
  	try:
  		return unicode(self.id)  # python 2

  	except NameError:
  		return str(self.id)  # python 3

  def __repr__(self):
   	return '<User %r>' % (self.username)    
     

#@lm.user_loader
#def load_user(id):
    #return User.query.get(int(id))



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
        if request.form['username'] == "" or request.form['password'] == "" or request.form['email'] == "" or request.form['firstname'] == "" or request.form['lastname'] == "":
                error = 'Please fill all fields. Thank you.'

        else:
        	#Create a new entry in the heroku postgres database
        	try:      		
        	    newUser = User(request.form['firstname'],request.form['lastname'], request.form['username'], request.form['email'], request.form['password'])
        	    db.session.add(newUser)
        	    db.session.commit()

        	except Exception as e:
        		error = "There was a problem with our database. Please try again."
        		print "EXCEPTION: " + e.message
        		return render_template('register.html', error=error)


    return render_template('register.html', error=error)


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

@app.route('/about' ,methods=['GET', 'POST'] )
def aboutUs():
	return render_template('aboutus.html')



if __name__ == '__main__':
    app.run()
