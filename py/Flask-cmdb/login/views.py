#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, redirect, render_template, session, url_for
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import models

login = Blueprint('login', __name__,  url_prefix='/login', template_folder='templates', static_folder='static')

# session 验证
from functools import wraps

def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args, **kwargs)
        return rtn
    return wapper


#访问登录页面/login/现在是这里
@login.route('/')
def index():
    return render_template('login.html')


#登出
@login.route('/Exit/')
@login_required
def Exit():
    session.pop('user', None)
    #return redirect('/')
    return redirect(url_for('login.index'))


#登录验证这里是login/login//,第一个/login椒url_prefix,在bp里面所有请求url=url_prefix+app.route(urlband)
@login.route('/login/', methods=['POST'])
def log():
#现在才执行到这个位置
    #ni xian zai zhi chuli post qing qiu ne
    username = request.form.get('username')
    password = request.form.get('password')
    if models.mysql_userlogin(username, password):
        # 成功则显示所有用户的信息列表
        session['user'] = { 'username' : username }
        #return redirect('/user/')
        return redirect(url_for('login.user'))
    else:
        return render_template('login.html', \
                    Loginerror='用户名或密码错误', \
                    Loginusername=username, \
                    Loginpassword=password)


#验证用户名密码后，展示内容
@login.route('/user/', methods=['GET','POST'])
@login_required
def user():
    if request.method == 'GET':
        if session.get('user') is None:
            return redirect('/')
        else:
            body = models.mysql_cat()
            return render_template('bodys.html', pages=body)
    else:
        return "显示错误"

























