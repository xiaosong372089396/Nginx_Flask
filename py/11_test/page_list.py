#!/usr/bin/env python
# -*- coding:utf-8 -*-

import gconf
import math

class Page_list(object):
	_default_page_size = gconf.PAGE_SIZE
	_max_page_select = 5

	
	@classmethod
	def create_pagelist(cls, pageNum, pageSize, TotalNum):
		# 获取总共次数向上取整，每页显示数量，计算总共可以有多少页
		pageSize = int(pageSize) if str(pageSize).isdigit() else cls._default_page_size
		pageSize = cls._default_page_size if pageSize <= 5 or pageSize >= 100 else pageSize
		# 总共页数，分页信息，获取点击页数，如果为None,则默认为1
		_max_page_num = int(math.ceil(TotalNum * 1.0 / pageSize))
		pageNum = int(pageNum) if str(pageNum).isdigit() else 1
		# 判断点击页数小于等于0，如果是默认显示到第一页，否则跟着页数走
		pageNum = 1 if pageNum < 1 or pageNum > _max_page_num else pageNum
		# 如果-1,意思就是从0开始， 如果不减第一页就是1 * num, * 每一页显示数量
		_offset = (pageNum - 1) * pageSize
		#### sql = "select * from asset limit %s, %s" % (_offset, _limit)
		
		# 开始页数，等于参数pageNum值
		_start_page_num = pageNum
		# 结束和开始一致
		_end_page_num = pageNum
		for _page in range(1, cls._max_page_select):  #最大查看页数
			if _start_page_num > 1:  #如果开始页数>1, 则-1从当前页数计算
				_start_page_num -= 1
			if _end_page_num < _max_page_num:
				_end_page_num += 1
			
			if _end_page_num - _start_page_num + 1 >= cls._max_page_select:
				break
		return cls(pageNum, pageSize, TotalNum, _max_page_num, _start_page_num, _end_page_num)
		
	def __init__(self, pageNum, pageSize, TotalNum, max_PageNum, startPageNum, endPageNum):
		self.pageNum = pageNum 
		self.pageSize = pageSize
		self.TotalNum = TotalNum
		self.max_PageNum = max_PageNum
		self.startPageNum = startPageNum
		self.endPageNum = endPageNum
	
	def set_contents(self, contents=[]):
		self.contents = contents
	
	def __str__(self):
		return str(self.__dict__)
		
		
		
		


		
		
