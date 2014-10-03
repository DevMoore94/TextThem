import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import requests

#create app
app = Flask(__name__)

@app.route('/')
def home_page():
    
    error = None
    if request.method == 'POST':
		
		if(request.form['number'] == "" or request.form['message']):
			error = "ERROR: Please fill in the above fields"
		else:
			requests.post(os.environ['BLOWERIO_URL'] + '/messages', data={'to': '+' + [request.form['number'], 'message': [request.form['message']})



	return render_template('layout.html', error=error)


if __name__ == '__main__':
    app.run()