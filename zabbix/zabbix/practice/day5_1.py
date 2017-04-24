#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
一个list[(1,4),(5,1),(2,3)],根据每个元组中的较大值进行排序
期待结果：[(2,3),(1,4),(5,1)]
要求：用sorted和lambda完成
级别1：在lambda中用max
级别2：lambda中不用max
'''

list_data = [(1,4),(5,1),(2,3)]
#级别1：在lambda中用max
print sorted(list_data,key = lambda x: max(x))
#级别2：lambda中不用max
print sorted(list_data, key = lambda x:x if x[0] > x[1] else x[1])
