# -*- coding:utf-8 -*-
import os
import urllib2
from datetime import datetime

from flask import request, flash, url_for, redirect, render_template, g,\
session, json, send_from_directory

from flask.ext.login import LoginManager, current_user, logout_user, \
login_user, login_required

from mindmap import app, db, login_manager

import traceback

@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/reciteWord.html')
def index():
    import requests
    real_link = "http://localhost/book.txt"
    r = requests.get(real_link)
    books = []
    for line in r.iter_lines():
        if not line:
            continue
        items = line.split()
        if len(items) == 2:
            name, link = items
            num = ""
        else:
            name, link, num = items
        #app.logger.debug(line)
        books.append({'name': name, 'link': link, 'num': num})
    #app.logger.debug(books)
    return render_template('reciteWord.html', books = books)

@app.route('/login',methods=['GET','POST'])
def login():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    pass

@app.route('/recommendlist')
@app.route('/recommendlist.html')
def recommendlist():
    pass

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.before_request
def before_request():
    g.user = current_user
