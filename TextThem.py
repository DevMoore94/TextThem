import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

#create app
app = Flask(__name__)

@app.route('/')
def home_page():
    
    return render_template('layout.html')


if __name__ == '__main__':
    app.run(debug=True)