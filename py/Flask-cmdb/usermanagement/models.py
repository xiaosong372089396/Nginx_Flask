#!/usr/bin/env python
#-*- coding:utf-8 -*-


import MySQLdb as mysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#from ..gconf import gconf
sys.path.append("..")
import gconf

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


#根据用户主键删除用户信息
SQL_DELETE_BY_ID = 'DELETE FROM user where id=%s;'
def delete_user(uid):
    conn = mysql.connect(host=gconf.DB_HOST, \
                     port=gconf.DB_PORT, \
                     user=gconf.DB_USER, \
                     passwd=gconf.DB_PASS, \
                     db=gconf.DB_DATABASE, \
                     charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    count = cur.execute(SQL_DELETE_BY_ID, (uid,))
    conn.commit()
    cur.close()
    conn.close()
    return count != 0


#用户管理修改
def mysql_update(password, age, email, IPhone, username):
    conn = mysql.connect(host=gconf.DB_HOST, \
                    port=gconf.DB_PORT, \
                    user=gconf.DB_USER, \
                    passwd=gconf.DB_PASS, \
                    db=gconf.DB_DATABASE, \
                    charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    count = cur.execute('update user set password=%s, age=%s, email=%s, IPhone=%s where username=%s', \
    (password, age, email, IPhone, username))
    conn.commit()
    return count != 0

#select * from user where username='xiaosong';

#update user set password='123.com', age=26, email='567@.com', IPhone='7890' where username="xiaoliu";

#查找某个用户名的详细信息
def mysql_select(username):
    conn = mysql.connect(host=gconf.DB_HOST, \
                port=gconf.DB_PORT, \
                user=gconf.DB_USER, \
                passwd=gconf.DB_PASS, \
                db=gconf.DB_DATABASE, \
                charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    SQL = "select * from asset where hostname='%s';" % username
    cur.execute(SQL)
    data = cur.fetchall()
    return data
    cur.close()
    conn.close()

#SELECT * FROM user where username='xiaoliu';


