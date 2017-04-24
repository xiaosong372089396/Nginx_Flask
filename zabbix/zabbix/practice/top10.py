#!/usr/bin/env python
#-*- coding:utf-8 -*-

log_stat_dict = {}
handle = open('/srv/salt/www_access_20140823.log')
'''
打开文件读取一行
readline()
readlines()
for line in handle
'''

while True:
    _line = handle.readline()   #读取一行
    #判断文件是否已经完成
    if '' == _line:
        break
    #解析每一行
    _log_nodes = _line.split()
    _ip = _log_nodes[0]
    _url = _log_nodes[6]
    _code = _log_nodes[8]

    _key = (_ip,_url,_code)
    log_stat_dict.setdefault(_key,0)
    log_stat_dict[_key] += 1        #log_stat_dict[_key] = log_stat_dict[_key] + 1

handle.close()

#dic => list
'''items()
[((ip,url,code),value),((ip, url, code), value)]
'''

log_stat_list = []
for _key in log_stat_dict:
    _value = log_stat_dict[_key] #log_stat_dict.get(_key,None)
    _ip, _url, _code = _key     #_ip,_url,_code = _key[0], _key[1], _key[2]
    log_stat_list.append([_code, _url,(_ip, _value)])

for j in range(10):
    for i in range(len(log_stat_list) - 1):
        if log_stat_list[i][2][1] > log_stat_list[i + 1][2][1]:
            log_stat_list[i],log_stat_list[i + 1] = log_stat_list[i + 1],log_stat_list[i]

for node in log_stat_list[:-11:-1]:
    print node

   
