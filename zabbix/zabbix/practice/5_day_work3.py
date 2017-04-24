#!/usr/bin/env python
# -*- coding:utf-8 -*-


a = [(1,4),(5,1),(2,3)]
b = sorted(a, key=lambda x:(x[0] > x[1] and x[0] or x[1]))
print b

