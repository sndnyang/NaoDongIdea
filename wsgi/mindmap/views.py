# -*- coding:utf-8 -*-
import os
import random
import urllib2
from datetime import datetime

from flask import request, flash, url_for, redirect, render_template, g,\
session, json, send_from_directory

from flask.ext.login import LoginManager, current_user, logout_user, \
login_user, login_required

from mindmap import app, db, login_manager

@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/reciteWord.html')
def index():
    import requests
    real_link = "http://localhost/books.txt"
    real_link = "http://7xt8es.com1.z0.glb.clouddn.com/naodong/word/books.txt?v=" \
                + str(random.randint(1, 10000))
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

@app.route('/getWords/<book>', methods=["GET"])
@login_required
def getWords(book):

    try:
        wordDict = ReciteWord.query.filter_by(book_name=book.strip(), user_id=g.user.get_id()).one_or_none()
    except sqlalchemy.orm.exc.MultipleResultsFound:
        return u'重复数据异常'
    data = wordDict.get_data() if wordDict else {}
    return json.dumps(data, ensure_ascii=False)


@app.route('/putWords', methods=["POST"])
@login_required
def putWords():
    book = request.json.get('book', None)
    data = request.json.get('data', None)

    if not book or not data:
        return json.dumps({})

    try:
        word_dict = ReciteWord.query.filter_by(book_name=book.strip(), user_id=g.user.get_id()).one_or_none()
    except sqlalchemy.orm.exc.MultipleResultsFound:
        return json.dumps({'error': u'重复数据异常'})

    if word_dict is None:
        new_word_user = ReciteWord(g.user.get_id(), book.strip(), data)
        db.session.add(new_word_user)
        db.session.commit()
    else:
        stored_data = word_dict.data
        new_data = data
        for k in stored_data:
            if k not in new_data:
                new_data[k] = {}
            for e in stored_data[k]:
                if e not in new_data[k]:
                    new_data[k][e] = stored_data[k][e]

        word_dict.data = new_data
        db.session.commit()

    return json.dumps({})
    
    
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
