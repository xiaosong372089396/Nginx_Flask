#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, redirect, render_template, session 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import models

app = Flask(__name__)

#访问登录页面
@app.route('/')
def index():
    return render_template('login.html')

#登录
@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password') 
    if models.mysql_userlogin(username, password):
        return redirect('/user/')
    else:
        return render_template('login.html', \
                   Loginerror='用户名或密码错误', \
                   Loginusername=username, \
                   Loginpassword=password)

#注册：
@app.route('/register/', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        username = request.args.get('username')
        password = request.args.get('password')
        age = request.args.get('age')
        email = request.args.get('emial')
        IPhone = request.args.get('IPhone')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        email = request.form.get('email')
        IPhone = request.form.get('IPhone')
        sensitive_str = ['~','@','#','$','%','^','&','*','(',')','_','.']
        if username not in sensitive_str:
            if username != '' and password != '':
                if models.mysql_userlogin(username, password):
                    return render_template('login.html', \
                            registererror='用户名或密码存在', \
                            registerusername=username, \
                            registerpassword=password)
                else:
                        #age必须是数字，这里做下转换对应数据库中的int类型
                    if models.mysql_add(username, password, int(age), email, IPhone):
                        return redirect('/successful/') 
                    else:
                        return "注册失败"
            else:
                return render_template('login.html', \
                             Username='用户名或密码不能为空')
        else:
            return render_template('login.html', \
                sensitive_str='用户名含有敏感字符，请重新输入:')

#增加：
@app.route('/increase/', methods=['GET','POST'])
def increase():
    if request.method == 'POST':
        return render_template('increase.html')
        
@app.route('/increaseone/',methods=['GET','POST'])
def increaseone():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        email = request.form.get('email')
        IPhone = request.form.get('IPhone')
        if models.mysql_add(username, password, age, email, IPhone):
           # return render_template('bodys.html')
            return "添加成功"
        else:
            return "添加失败"

#删除:
@app.route('/delete/',methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        return render_template('delete.html')

@app.route('/deleteone/',methods=['GET','POST'])
def deleteone():
    if request.method == 'POST':
         #根据ID来删除用户名
        username = request.form.get('username')
        data = models.mysql_select(username)
        for i in data:
        #根据ID来删除用户名
            id = i[0]
            if models.mysql_del(id):
                return "删除成功"
            else:
                return "删除失败"


#修改
@app.route('/update/', methods=['GET','POST'])
def genxin():
    if request.method == 'POST':
        return render_template('update.html')


@app.route('/updateone/',methods=['GET','POST'])
def option():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')
        age = request.form.get('age')
        email = request.form.get('email')
        IPhone = request.form.get('IPhone')
        if models.mysql_update(password, age, email, IPhone, username):
            return "修改成功"
        else:
            return "修改失败"

#查找
@app.route('/select/',methods=['GET','POST'])
def select():
    if request.method == 'POST':
        username = request.form.get('user')
        data = models.mysql_select(username)
        return render_template('select.html', pages=data)


#验证用户名密码后，展示内容
@app.route('/user/', methods=['GET','POST'])
def user():
    if request.method == 'GET':
        body = models.mysql_cat()
        return render_template('bodys.html', pages=body)
    else:
        return "显示错误"

#注册回显
@app.route('/successful/')
def successful():
    return "注册成功"
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

#版本1,在修改. 修改后提交
