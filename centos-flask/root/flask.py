#!/usr/bin/python3 
import os
from flask import Flask
app = Flask(__name__)

from flask import render_template
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def hello(name=None):
    return render_template('hello.html', hostname=os.getfqdn())

