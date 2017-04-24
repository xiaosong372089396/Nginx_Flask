#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb as mysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")
import gconf


#用户登录验证：
def mysql_userlogin(username, password):
    conn = mysql.connect(host=gconf.DB_HOST, \
                       port=gconf.DB_PORT, \
                        user=gconf.DB_USER, \
                       passwd=gconf.DB_PASS, \
                        db=gconf.DB_DATABASE, \
                       charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    SQL = "select * from user where username='%s' and password='%s'" % (username, password)
    count = cur.execute(SQL)
    cur.close()
    conn.close()
    return count != 0


#添加：
def mysql_add(username, password, age, email, IPhone):
    conn = mysql.connect(host=gconf.DB_HOST, \
                   port=gconf.DB_PORT, \
                   user=gconf.DB_USER, \
                   passwd=gconf.DB_PASS, \
                   db=gconf.DB_DATABASE, \
                   charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    count = cur.execute('insert into user (username, password, age, email, IPhone) values(%s, %s, %s, %s, %s)', \
    (username, password, age, email, IPhone))
    conn.commit()
    cur.close()
    conn.close()
    return count != 0


#获取全部信息
def mysql_cat():
    user_dic = {}
    conn = mysql.connect(host=gconf.DB_HOST, \
              port=gconf.DB_PORT, \
              user=gconf.DB_USER, \
              passwd=gconf.DB_PASS, \
              db=gconf.DB_DATABASE, \
              charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    sql_select = "select * from user;"
    cur.execute(sql_select)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data