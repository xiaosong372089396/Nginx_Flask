#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb as mysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#from ..gconf import gconf
sys.path.append("..")
import gconf


# 获取zabbix主机信息数量值
def get_zabbix_count():
    conn = mysql.connect(host=gconf.DB_HOST, \
                        port=gconf.DB_PORT, \
                        user=gconf.DB_USER, \
                        passwd=gconf.DB_PASS, \
                        db=gconf.DB_ZABBIX, \
                        charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    SQL = "select count(*) from hosts where host like '192%'";
    cur.execute(SQL)
    data = cur.fetchall()
    cur.close()
    conn.close()
    for row in data:
        num = row[0]
        return num

#分页数据库offset=页数， limit=每页显示条数
def get_zabbix_host(offset=None, limit=None):
    conn = mysql.connect(host=gconf.DB_HOST, \
                          port=gconf.DB_PORT, \
                          user=gconf.DB_USER, \
                          passwd=gconf.DB_PASS, \
                          db=gconf.DB_ZABBIX, \
                         charset=gconf.DB_CHARSET)
    cur = conn.cursor()
#    sql = "SELECT * FROM hosts where host like '192%' limit %s,%s;" %(offset, limit)
    sql = "SELECT * FROM hosts where host limit %s,%s;" %(offset,limit)
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# 获取zabbix库中 hosts表中数据
#def zabbix_get():
#    conn = mysql.connect(host=gconf.DB_HOST, \
#                         port=gconf.DB_PORT, \
#                         user=gconf.DB_USER, \
#                         passwd=gconf.DB_PASS, \
#                         db=gconf.DB_ZABBIX, \
#                         charset=gconf.DB_CHARSET)
#    cur = conn.cursor()
#    sql = "select * from hosts where host like '192%';"
#    # select * from hosts where host like '192%';
#    cur.execute(sql)
#    data = cur.fetchall()
#    cur.close()
#    conn.close()
#    return data