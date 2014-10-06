import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import requests

#create app
app = Flask(__name__)

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
	return render_template('login.html')

@app.route('/about' ,methods=['GET', 'POST'] )
def aboutUs():
	return render_template('aboutus.html')



if __name__ == '__main__':
    app.run()
