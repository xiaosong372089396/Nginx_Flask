#!/usr/bin/env python


import salt.client

client = salt.client.LocalClient()
ret = client.cmd('*', 'cmd.run',['free -m; df -Th'])
for i,n in ret.items():
    print "'\t'%s,%s" %(i,n) 
