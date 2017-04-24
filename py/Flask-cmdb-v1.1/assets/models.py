#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import MySQLdb as mysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")
import gconf


#根据资产主键删除主机信息
SQL_DELETE_BY_ID_ASSET = 'DELETE FROM asset where id=%s;'
def delete_asset(uid):
    conn = mysql.connect(host=gconf.DB_HOST, \
                     port=gconf.DB_PORT, \
                     user=gconf.DB_USER, \
                     passwd=gconf.DB_PASS, \
                     db=gconf.DB_DATABASE, \
                     charset=gconf.DB_CHARSET)
    cur = conn.cursor()
   # count = cur.execute(SQL_DELETE_BY_ID, (uid,))
    count = cur.execute(SQL_DELETE_BY_ID_ASSET, (uid,))
    conn.commit()
    cur.close()
    conn.close()
    return count != 0


#追加资产管理
def add_asset(sn, ip, hostname, machine_room_id, bussiness, admin, cpu, ram, disk, os, model, purchase_date, vendor, statusa):
    conn = mysql.connect(host=gconf.DB_HOST, \
          port=gconf.DB_PORT, \
          user=gconf.DB_USER, \
          passwd=gconf.DB_PASS, \
          db=gconf.DB_DATABASE, \
          charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    sql = 'insert into asset (sn, ip, hostname, machine_room_id, bussiness, admin, cpu, ram, disk, os, model, purchase_date, vendor, status) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
    count = cur.execute(sql, (sn, ip, hostname, machine_room_id, bussiness, admin, cpu, ram, disk, os, model, purchase_date, vendor, statusa))
    conn.commit()
    cur.close()
    conn.close()
    return count != 0

#资产管理页面信息
#获取全部信息
def asset_cat():
    conn = mysql.connect(host=gconf.DB_HOST, \
                port=gconf.DB_PORT, \
                user=gconf.DB_USER, \
                passwd=gconf.DB_PASS, \
                db=gconf.DB_DATABASE, \
                charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    sql_select = "select * from asset;"
    cur.execute(sql_select)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


#资产管理修改
def assetsupdate(sn, ip, hostname, machine_room, bussiness, admin, cpu, ram, disk, os, model, purchase_date, vendor, statusb, id):
    conn = mysql.connect(host=gconf.DB_HOST, \
                        port=gconf.DB_PORT, \
                        user=gconf.DB_USER, \
                        passwd=gconf.DB_PASS, \
                        db=gconf.DB_DATABASE, \
                        charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    count = cur.execute('update asset set sn=%s, ip=%s, hostname=%s, machine_room_id=%s, bussiness=%s, admin=%s, cpu=%s, ram=%s, disk=%s, os=%s, model=%s, purchase_date=%s, vendor=%s, status=%s where id=%s', \
    (sn, ip, hostname, machine_room, bussiness, admin, cpu, ram, disk, os, model, purchase_date, vendor, statusb, id ))
    conn.commit()
    cur.close()
    conn.close()
    return count != 0

################################
def get_assets(offset=None, limit=None):
    conn = mysql.connect(host=gconf.DB_HOST, \
                          port=gconf.DB_PORT, \
                          user=gconf.DB_USER, \
                          passwd=gconf.DB_PASS, \
                          db=gconf.DB_DATABASE, \
                         charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    sql = "SELECT * FROM asset limit %s,%s" %(offset, limit)
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# 获取所有数量
def get_asset_count():
    conn = mysql.connect(host=gconf.DB_HOST, \
                        port=gconf.DB_PORT, \
                        user=gconf.DB_USER, \
                        passwd=gconf.DB_PASS, \
                        db=gconf.DB_DATABASE, \
                        charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    SQL = 'select count(*) from asset;'
    cur.execute(SQL)
    data = cur.fetchall()
    cur.close()
    conn.close()
    for row in data:
        num = row[0]
        return num




######################################################## echars 插入MySQL
def Moniter(mtime,ip, cpu, mem, disk):
    conn = mysql.connect(host=gconf.DB_HOST, \
                        port=gconf.DB_PORT, \
                        user=gconf.DB_USER, \
                        passwd=gconf.DB_PASS, \
                        db=gconf.DB_DATABASE, \
                        charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    data = cur.execute('insert into moniter(ip, cpu, mem, disk, mtime)values(%s, %s, %s, %s, %s)', \
    (ip,cpu,mem,disk, mtime))
    conn.commit()
    cur.close()
    conn.close()
    return data != 0


######取值
def getData(ip):
    conn = mysql.connect(host=gconf.DB_HOST, \
                       port=gconf.DB_PORT, \
                       user=gconf.DB_USER, \
                       passwd=gconf.DB_PASS, \
                       db=gconf.DB_DATABASE, \
                     charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    sql = 'select * from moniter where ip = %s and mtime >= %s order by mtime asc'
    mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 60 * 60))
    cur.execute(sql, (ip, mtime))
    data = cur.fetchall()
    times = []
    cpu_data = []
    mem_data = []
    disk_data = []
    cur.close()
    conn.close()
    for res in data:
        _cpu, _mem, _disk, _time = res[2], res[3], res[4], res[5]
        times.append(_time.strftime('%H:%M'))
        cpu_data.append(_cpu)
        mem_data.append(_mem)
        disk_data.append(_disk)
    return {'categories' : times, 'series' : [{'name' : 'cpu', 'data' : cpu_data}, {'name' : '内存', 'data' : mem_data}, {'name' : 'disk', 'data' :disk_data}]}


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



