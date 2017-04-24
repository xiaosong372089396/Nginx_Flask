#!/usr/bin/env python
#-*- coding:utf-8 -*-

import MySQLdb as mysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#from ..gconf import gconf
sys.path.append("..")
import gconf

#code, count
def get_code_distri():
    conn = mysql.connect(host=gconf.DB_HOST, \
                        port=gconf.DB_PORT, \
                        user=gconf.DB_USER, \
                        passwd=gconf.DB_PASS, \
                        db=gconf.DB_DATABASE, \
                      charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    sql = 'select code, count(*) from webaccess2 group by code;'
    cur.execute(sql)
    data = cur.fetchall()
    codes = []
    datas = []
    cur.close()
    conn.close()
    for name, value in data:
        codes.append(str(name))
        datas.append({'name' : str(name), 'value' : value })
    return codes, datas

##logdates, data_logdate
def get_code_distri_logdate():
    conn = mysql.connect(host=gconf.DB_HOST, \
                          port=gconf.DB_PORT, \
                          user=gconf.DB_USER, \
                          passwd=gconf.DB_PASS, \
                          db=gconf.DB_DATABASE, \
                          charset=gconf.DB_CHARSET)
    cur = conn.cursor()
    sql = r"select DATE_FORMAT(logdate, '%%Y-%%m-%%d %%H:00:00'), code, count(*) from webaccess2 group by code, DATE_FORMAT(logdate, '%%Y-%%m-%%d %%H:00:00');"
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    logdates = []
    datas = {}
    """
    +-----------------------------------------------+------+----------+
    | DATE_FORMAT(logdate, '%%Y-%%m-%%d %%H:00:00') | code | count(*) |
    +-----------------------------------------------+------+----------+
    | %Y-%m-%d %H:00:00                             |  200 |     5871 |
    | %Y-%m-%d %H:00:00                             |  206 |        4 |
    | %Y-%m-%d %H:00:00                             |  301 |        2 |
    | %Y-%m-%d %H:00:00                             |  304 |      720 |
    | %Y-%m-%d %H:00:00                             |  403 |        1 |
    | %Y-%m-%d %H:00:00                             |  404 |      226 |
    +-----------------------------------------------+------+----------+
    """
    #遍历这个元组，根据位置分别传值给对应元素
    for logdate, code, count in data:
    #日期时间如果不在这个列表中，则添加。区分表中新数据时间
        if logdate not in logdates:
            logdates.append(logdate)
        #如果这个键在字典中，则key是code,如果不在赋予空
        #{200: {}}
        datas.setdefault(code, {})
        #然后给这个key,赋予values
        #{ 200: {'%Y-%m-%d %H:00:00' : 5871 }}
        datas[code][logdate] = count
    #最后列表正向排序
    logdates.sort()
    print logdates
    data_logdate = []
    #遍历格式
    # for code, count in dates.items()
    # print code, count
    # 1 {'%Y-%m-%d %H:00:00': 5871}
    for code, count in datas.items():
        _temp = {'name' : code, 'type' : 'bar', 'stack' : 'code','data' :[]}
        #遍历列表时间，然后_temp  data属性添加count获取logdate时间戳,如没有则赋值0
        for logdate in logdates:
            _temp['data'].append(count.get(logdate, 0))
         #列表追加_temp里key data的值 时间
        data_logdate.append(_temp)
    #返回时间戳列表和属性值列表
    return logdates, data_logdate

