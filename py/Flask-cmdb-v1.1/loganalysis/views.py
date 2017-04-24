#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, redirect, render_template, session
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
import models

# session 验证
from functools import wraps

loganalysis = Blueprint('loganalysis', __name__, url_prefix='/loganalysis', template_folder='templates', static_folder='static')

def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args, **kwargs)
        return rtn
    return wapper



################log
@loganalysis.route('/Loganalysis/', methods=['GET'])
@login_required
def logs():
    #状态码和次数
    codes, datas = models.get_code_distri()
    #时间，属性值
    logdates, data_logdate = models.get_code_distri_logdate()
    print logdates
    print data_logdate
    return render_template('Loganalysis.html', \
        codes = json.dumps(codes), datas=json.dumps(datas), \
        logdates=json.dumps(logdates), datas_logdate=json.dumps(data_logdate))









































