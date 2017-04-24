#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect
import logfile

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def logindex():
    #判断访问的方式：
    if request.method == "GET":
    #如果访问方式是GET，要获取表单信息，就要args.get方法：
        name = request.args.get('username')
        password = request.args.get('password')
    else:
    #如果是POST方式，就用form.get方式获取
        name = request.form.get('username')
        password = request.form.get('password')
    #然后在第一次访问时候是GET,在填写完用户名，密码提交后，访问方式变成POST，所以格式是这样，然后进行判断用户名，密码
    if name == 'xiaoxiao' and password == 'xiaoxiao':
        #重定向到路由/logs/的地方：
        return redirect('/logs/')
    #如果用户名，密码其中一个不匹配，则返回表单，让重新输入
    return render_template('login.html', error='login fail')



@app.route('/logs/')
def logs():
    #导入了分析Nginx脚本，用脚本调用里面的函数方法：   
    stat_dict = logfile.logfile('www_access_.log')
    #用脚本调用里面方法，15是想查看的Nginx top 值
    result_list = logfile.datalist(stat_dict, 15)
    #执行完的结果，则返回log.html页面去展示，result_list得到的是一个没有排序过的列表，
    #把值赋值给logs，供log.html页面调用
    return render_template('log.html', logs=result_list);

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)
