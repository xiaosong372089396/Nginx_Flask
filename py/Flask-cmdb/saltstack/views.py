#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, redirect, render_template, session
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from functools import wraps
import os

saltstack = Blueprint('saltstack',__name__, url_prefix='/saltstack', template_folder='templates', static_folder='static')

def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args, **kwargs)
        return rtn
    return wapper


# Saltstack API集成
@saltstack.route('/installation/', methods=['GET','POST'])
@login_required
def installation():
    import saltapi
    if request.method == 'POST':
        ip = request.form.get('ip')
        Fun = request.form.get('Option')
        arg = request.form.get('arg')
        cls_ = saltapi.salt_api()
        command = cls_.main(ip, Fun, arg)
        return render_template('installation.html', Value=command)
    else:
        if request.method == 'GET':
            return render_template('installation.html')

# Saltstack 在线编辑States文件，然后上传到minions目录下：
@saltstack.route('/editor/', methods=['GET', 'POST'])
@login_required
def editor():
    headimg = os.path.join(os.getcwd(), 'minions/')
    if request.method == 'POST':
        state_id = request.form.get('state_id')

    else:
        return render_template('editor.html')
































