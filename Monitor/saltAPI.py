#!/usr/bin/env python
# -*- coding:utf-8 -*-


import salt.client


client = salt.client.LocalClient()
ret = client.cmd('*', 'test.ping')
for i,n in ret.items():
    print "'\t'%s,'\t'\033[1;42m;%s\033[0m" %(i,n) 
