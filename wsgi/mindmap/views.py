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
        # app.logger.debug(line)
        books.append({'name': name, 'link': link, 'num': num})
    app.logger.info(books)
    print books
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        if User.query.filter_by(username=username).first():
            flash(u'该用户名已被注册')
            meta = {'title': u'注册 知维图 -- 互联网学习实验室',
                    'description': u'知维图--试图实现启发引导式智能在线学习，数学与计算机领域',
                    'keywords': u'zhimind mindmap 思维导图 启发式学习 智能学习 在线教育'}
            return render_template('register.html', form=form, meta=meta)

        code_text = session['code_text']

        if form.code.data == code_text:
            user = User(username, request.form['password'], request.form['email'])
            try:
                db.session.add(user)
                db.session.commit()
                flash('User successfully registered')
                return redirect(url_for('login'))
            except:
                db.session.rollback()
                flash(u'注册失败')
        else:
            flash(u'验证码错误')
    meta = {'title': u'注册 知维图 -- 互联网学习实验室',
            'description': u'知维图--试图实现启发引导式智能在线学习，数学与计算机领域',
            'keywords': u'zhimind mindmap 思维导图 启发式学习 智能学习 在线教育'}
    return render_template('register.html', form=form, meta=meta)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        meta = {'title': u'登录 知维图 -- 互联网学习实验室',
                'description': u'知维图--试图实现启发引导式智能在线学习，数学与计算机领域',
                'keywords': u'zhimind mindmap 思维导图 启发式学习 智能学习 在线教育'}
        return render_template('login.html', meta=meta)

    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True

    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user, remember=remember_me)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>')
def get_user(nickname):
    user = User.query.filter_by(username=nickname).first()
    if not user:
        flash(u'不存在用户：' + nickname + '！')
        return redirect(url_for('index'))

    mind_maps = None
    try:
        mind_maps = MindMap.query.filter_by(user_id=user.get_id()).all()
    except:
        app.logger.error("use " + nickname + " fetch maps failed")

    tutorials = None
    try:
        tutorials = Tutorial.query.filter_by(user_id=user.get_id()).all()
    except:
        app.logger.error("use " + nickname + " fetch tutorials failed")

    meta = {'title': u'用户 %s 主页 知维图 -- 互联网学习实验室' % nickname,
            'description': u'知维图--试图实现启发引导式智能在线学习，数学与计算机领域',
            'keywords': u'zhimind mindmap 思维导图 启发式学习 智能学习 在线教育'}
    return render_template('user.html', user=user, maps=mind_maps,
                           tutorials=tutorials, isSelf=user.get_id() == g.user.get_id(),
                           meta=meta)


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.before_request
def before_request():
    g.user = current_user


@app.errorhandler(404)
def page_not_found(error):
    meta = {'title': u'页面不存在 知维图 -- 互联网学习实验室',
            'description': u'知维图--试图实现启发引导式智能在线学习，数学与计算机领域',
            'keywords': u'zhimind 启发式学习 智能学习 在线教育'}
    return render_template('404.html', meta=meta)
