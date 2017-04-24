#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, redirect, render_template, session,url_for
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import models
import json
from functools import wraps

user = Blueprint('usermanagement', __name__, url_prefix='/usermanagement', template_folder='templates', static_folder='static')
#
def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args, **kwargs)
        return rtn
    return wapper


#用户管理页面
@user.route('/usermanagement/', methods=['POST', 'GET'])
@login_required
def bodyuser():
    if request.method == 'GET':
        #if session.get('user') is None:
        #   return redirect('/')
        #   return redirect(url_for('login.log'))
        #else:
        body = models.mysql_cat()
        return render_template('usermanagement.html', pages=body, name=session.get('user'))
    else:
        return "显示错误"


# 添加用户信息(添加到DB)
@user.route('/adduser/', methods=['POST'])
@login_required
def adduser():
    username = request.form.get('username','')
    password = request.form.get('password','')
    age = request.form.get('age','')
    email = request.form.get('email','')
    iphone = request.form.get('iphone','')
    if models.mysql_add(username, password, age, email, iphone):
        ok = True
        result = '添加成功'
        return json.dumps({ 'ok' : ok, 'result': result })
    else:
        ok = False
        result = '添加失败'
        return json.dumps({ 'ok' : ok, 'result' : result })


#删除:
#根据用户管理ID删除信息：
@user.route('/deleteuser/', methods=['GET', 'POST'])
@login_required
def deleteuser():
    if request.method == 'POST':
        _id = request.form.get('id')
        if  models.delete_user(_id):
            ok = True
            result = '删除成功'
            return json.dumps({ 'ok' : ok, 'result': result  })
        else:
            ok = False
            result = '删除失败'
            return json.dumps({ 'ok' : ok, 'result' : result })
    return redirect('/user/')


#用户管理修改
@user.route('/updateone/',methods=['GET','POST'])
@login_required
def option():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        email = request.form.get('email')
        iphone = request.form.get('iphone')
        if models.mysql_update(password, age, email, iphone, username):
            ok = True
            result = '修改成功'
            return json.dumps({ 'ok' : ok, 'result': result })
        else:
            ok = False
            result = '修改失败'
            return json.dumps({ 'ok' : ok, 'result' : result })



































