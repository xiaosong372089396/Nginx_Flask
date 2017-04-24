#!/usr/bin/env python
#-*- coding:utf-8 -*-

dic = {}
f = open('/srv/salt/www_access_20140823.log','r')
'''
打开文件读取一行
readline()
readlines()
for line in handle
'''
while True:
    handle = f.readline() #读取一行
    #判断文件是否已经完成
    if '' == handle:
        break
    #解析每一行    
    logfile = handle.split()
    status = logfile[8]
    url = logfile[6]
    ip = logfile[0]
    key = (ip, url, status)
    dic.setdefault(key, 0)
    dic[key] += 1      #dic[key] = dic[key] + 1
f.close()

#dic => list
'''
items()
[((ip,url,status),((ip, url, status), value))]
'''
data_list = []
for _key  in dic:
    _value = dic[_key]    #dic.get(key,None)
    ip, url, status = _key  #ip,url,status = _key[0],_key[1],_key[2]
    data_list.append([status, url,(ip, _value)])

for i in range(10):
    for o in range(len(data_list) -1):
        if data_list[o][2][1] > data_list[o + 1][2][1]:
            data_list[o],data_list[o + 1] = data_list[o + 1], data_list[o]

for node in data_list[:-11:-1]:
    print node





