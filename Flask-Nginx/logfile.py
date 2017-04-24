#!/usr/bin/env python
#-*- coding:utf-8 -*-
 


dic_data = {}
list_data = []

def logfile(name):
    handle = open(name,'r')
    while True:
        log = handle.readline()
        if '' == log:
            break
        logfile = log.split()
        ip = logfile[0]
        url = logfile[6]
        status = logfile[8]
        all = (ip, url, status) 
        dic_data.setdefault(all, 0)
        dic_data[all] += 1
    handle.close()
    return dic_data

def datalist(key, n=10):
    for _key in key:
        if '' == _key:
            break
        value = dic_data[_key]
        ip, url, status = _key
        list_data.append([status, url,(ip,value)])
    for j in range(n):
        for i in range(len(list_data) - 1):
            if list_data[i][2][1] > list_data[i + 1][2][1]:
                list_data[i],list_data[i + 1] = list_data[i + 1],list_data[i]
#    for i in list_data[:-n - 1 :-1]:
#        print i
    #这里返回的是一个没有排过序的列表
    return list_data[:-n -1:-1]

if __name__ == '__main__':
    number = int(raw_input('Please input int number >'))
    datalist(logfile('www_access_.log'),number)

 
     
