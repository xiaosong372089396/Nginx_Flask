#!/usr/bin/env python
#-*- coding:utf-8 -*-

import math
import gconf

class PageList(object):
    _default_page_size = gconf.PAGE_SIZE
    #第一页到末页相隔页数计算
    _max_page_select = 5

    @classmethod
    def create_pagelist(cls, pageNum, pageSize, totalNum):
        # pageSize转换字符串， 然后方法检测字符串是否由数字组成, 如果不是，则使用默认数量
        pageSize = int(pageSize) if str(pageSize).isdigit() else cls._default_page_size
########
        #判断每页数量<=5 or >=100, 则pageSize等于默认页数,  否则等于传入参数值
        pageSize = cls._default_page_size if pageSize <= 5 or pageSize >= 100 else pageSize
########
        #转换整数，向上取整，除每页数量，获取一共的页数
        _max_page_num = int(math.ceil(totalNum * 1.0 / pageSize ))

######## 判断传进来的页数值监测字符串是否由数字组成，默认从第一页开始
        pageNum = int(pageNum) if str(pageNum).isdigit() else 1

########  判断pageNum值，< 1 or pageNum > _max_page_num , 否则值就是开始页数pageNum参数值
        pageNum = 1 if pageNum < 1 or pageNum > _max_page_num else pageNum

######## 如果-1, 意思就是从0开始，如果不减 第一页就是1 * num, * 每一页显示数量
        _offset = (pageNum - 1) * pageSize

        # 开始页数，等于参数pageNum值
        _start_page_num = pageNum
        # 结束和开始一致
        _end_page_num = pageNum
        for _page in range(1, cls._max_page_select):  #最大查看页数
            if _start_page_num > 1:     # 如果开始页数>1, 则-1从当前页数计算
                _start_page_num -= 1
            if _end_page_num < _max_page_num:
                _end_page_num += 1
########
            if _end_page_num - _start_page_num + 1 >= cls._max_page_select:
                break

        return cls(pageNum, pageSize, totalNum, _max_page_num,_start_page_num,_end_page_num),_offset

    def __init__(self,pageNum, pageSize, totalNum, maxPageNum, startPageNum, endPageNum ):
        self.pageNum = pageNum
        self.pageSize = pageSize
        self.totalNum = totalNum
        self.maxpageNum = maxPageNum
        self.startPageNum = startPageNum
        self.endPageNum = endPageNum

    def set_contents(self, contents=[]):
        self.contents = contents

    def __str__(self):
        # 类型字典，存储所有类型成员信息， 对象字典，存储所有实例成员信息
        return str(self.__dict__)


