#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import geoip2
import geoip2.database
import MySQLdb as mysql

import gconf

dic_data = {}
list_data = []

def logfile(name):
    reader = geoip2.database.Reader('static/GeoLite2-City.mmdb')
    handle = open(name,'r')
    while True:
        log = handle.readline()
        if '' == log:
            break
        logfile = log.split()
        logdate = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(logfile[3][1:], '%d/%b/%Y:%H:%M:%S'))
        ip = logfile[0]
        url = logfile[6]
        status = logfile[8]
        try:
            geo = reader.city(ip)
        except BaseException as e:
#        if geo.country.name != 'China':
            print geo.country.name
            print e
            continue
        address = geo.city.names.get('zh-CN','')
                  #geo = geo.city.names['zh-CN']
        lat = geo.location.latitude
        lot = geo.location.longitude
        print logdate, ip, url, status, address, lat,lot
        insert2db(logdate,ip,url,status,address,lat,lot)
           # break
    handle.close()
    return None

def insert2db(logdate,ip,url,code,address, lat, lot):
    conn = mysql.connect(host=gconf.DB_HOST, \
                           port=gconf.DB_PORT, \
                           user=gconf.DB_USER, \
                           passwd=gconf.DB_PASS, \
                           db=gconf.DB_DATABASE, \
                          charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    _sql = 'insert into webaccess2(logdate,ip,url,code,address,latitude,longitude)values(%s, %s, %s, %s, %s, %s, %s )'
    _args = (logdate, ip, url, code, address, lat, lot)
    data = cur.execute(_sql, _args)
    conn.commit()
    cur.close()
    conn.close()
    return data != 0

if __name__ == '__main__':
    logfile('/srv/salt/www_access_20140823.log')
