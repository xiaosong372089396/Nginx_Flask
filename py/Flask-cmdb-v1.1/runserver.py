#!/usr/bin/env python
#-*- coding:utf-8 -*-

from  flask import Flask

from assets import views as assets
from loganalysis import views as loganalysis
from login import views as login
from usermanagement import views as usermanagement
from zabbix import views as zabbix
from saltstack import views as saltstack


app =  Flask(__name__)
app.secret_key = 'xiaosong'

if __name__ == '__main__':
    app.register_blueprint(assets.assets)
    app.register_blueprint(loganalysis.loganalysis)
    app.register_blueprint(login.login)
    app.register_blueprint(usermanagement.user)
    app.register_blueprint(saltstack.saltstack)
    app.register_blueprint(zabbix.Zabbix)
    print app.url_map
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)