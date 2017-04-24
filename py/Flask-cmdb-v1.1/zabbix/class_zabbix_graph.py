#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import json
import sys
import urllib2
import logging
from urllib2 import URLError

logger = logging.getLogger(__name__)

class tools(object):
    
    def __init__(self):    
        self.zabbix_url = 'http://192.168.10.87:8088/zabbix/api_jsonrpc.php'
        self.login_url  = 'http://192.168.10.87:8088/zabbix/'
        self.graph_url  = 'http://192.168.10.87:8088/zabbix/chart2.php'
        self.zabbix_user = 'Admin'
        self.zabbix_pawd = '372089396'
        self.header = {"Content-Type":"application/json"}
        self.authid = self.auth()

    def auth(self):   
        pre_data = {
            "jsonrpc" : "2.0",
            "method" : "user.login",
            "params" : {
                 "user" : self.zabbix_user,
                 "password" : self.zabbix_pawd
                },
            "auth": None,
            "id" : 0
        }

        json_data = json.dumps(pre_data)
        request = urllib2.Request(self.zabbix_url,json_data, self.header)
        response = urllib2.urlopen(request)
        html =  response.read()
        html_json = json.loads(html)
        return html_json['result']


    def get_data(self,data,hostip=""):
        request = urllib2.Request(self.zabbix_url,data,self.header)
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e,'reason'):
                print 'We failed to reach a server.'
                print 'Reason:',e.reason
            elif hasattr(e, 'code'):
                print 'The Server could not fulfill the request.'
                print 'Error code: ',e.code
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            return response


    def get_host(self):
        print "********************************"
        data = {
            "jsonrpc":"2.0",
            "method":"host.get",
            "params": {
                    "output" : ["hostid","name"],
                    "filter" : {
                             "host" : ""           
                    },
                 },
             "auth":self.authid,
             "id": 1
        }
        json_data = json.dumps(data)
        print "#################################"
        request = urllib2.Request(self.zabbix_url,json_data,self.header)
        response = urllib2.urlopen(request)
        html = response.read()
        html_json = json.loads(html)
        res = html_json['result']
        for host in res:
            print "\t","hostid:",host['hostid'],"\t","host_name:",host['name'].encode('UTF8')

    def get_hostgroup(self):
        data = json.dumps (
              {
                 "jsonrpc": "2.0",
                 "method": "hostgroup.get",
                 "params" : {
                 "output" :"extend",
                 "filter": {
                 }
                      
        },
           "auth": self.authid,
           "id": 1
        })   
        request = urllib2.Request(self.zabbix_url,data,self.header)
        response = urllib2.urlopen(request)
        html = response.read()
        html_json = json.loads(html)
        res =  html_json['result']
        for host in res:
            print "\t","HostGroup_id:",host['groupid'],"\t","HostGroup_name:",host['name'].encode('UTF8')
    
    def get_templated(self):
        print "**********************************"
        data = json.dumps (
               {
                  "jsonrpc": "2.0",
                  "method" : "template.get",
                  "params" : {
                      "output" : "extend",
                      "filter" : {
                      }
            },
            "auth" : self.authid,
            "id": 1
        })
        request = urllib2.Request(self.zabbix_url,data,self.header)
        response = urllib2.urlopen(request)
        html = response.read()
        html_json = json.loads(html)
        res = html_json['result']
        for host in res:
            print "\t","Templateid:",host['templateid'],"\t","Template_name:",host['name'].encode('UTF8')

    def add_host(self):
        print "***********************************"
        HostName = str(raw_input("Please input you HostName:"))
        Hostip = str(raw_input("\033[1;35;40m%s\033[0m" % 'Please Enter your:host_ip :'))
        Groupid = str(raw_input("\033[1;35;40m%s\033[0m" % 'Please Enter your:group_id :'))
        Templateid = str(raw_input("\033[1;35;40m%s\033[0m" % 'Please Enter your:template_id :'))
        data = json.dumps (
             {
                 "jsonrpc":"2.0",
                 "method" :"host.create",
                 "params" : {
                       "host" : HostName,
                       "interfaces": [
                            {
                                 "type" : 1,
                                 "main" : 1,
                                 "useip" : 1,
                                 "ip" : Hostip,
                                 "dns" : "",
                                 "port" : "10050"
                            }
                         ], 
                         "groups" : [
                          {
                                "groupid":Groupid
                          }
                      ],
                      "templates" : [
                          {
                                "templateid":Templateid
                          }
                      ],
              },
              "auth": self.authid,
              "id" : 6
           })
        res = self.get_data(data)
        print res
        print "添加主机 : \033[40m%s\031[0m \tid :\033[31m%s\033[0m" % (Hostip, res['result']['hostids'])


    def del_host(self):
        hostip = self.get_host()
        print hostip
        Hostid = str(raw_input("Please Enter the delete id:"))
        data = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"host.delete",
                "params": [
                    Hostid
                ],
                "auth":self.authid,
                "id" :1
        })
        res = self.get_data(data)
        print "删除主机: \033[40m%s\031[0m \tid :\033[31m%s\033[0m" % (Hostid, res['result']['hostids'])

    def get_graph(self):
        hostip = self.get_host()
        print hostip
        hostid = int(raw_input("Please Enter select hostid :"))
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method" : "graph.get",
                "params" : {
                    "hostids" : hostid,
                    "sortfield" : "name"
                },
                "auth": self.authid,
                "id" : 1
        })
        request = urllib2.Request(self.zabbix_url, data, self.header)
        response = urllib2.urlopen(request)
        html = response.read()
        html_json = json.loads(html)
        result = html_json['result']
        for res in result:
            print "\t","graphid:", res['graphid'],"\t","graphname:", res['name'].encode('UTF8') 

    def get_graphid(self, graphid):
        import cookielib
        import time
        import urllib
        Stime = time.strftime( '%Y%m%d%H%M%S', time.localtime() )
        login_data = urllib.urlencode({
                    "name" : self.zabbix_user,
                    "password" : self.zabbix_pawd,
                    "autologin": 1,
                    "enter" : "Sign in" })
        #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie            
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        try:
            respone = opener.open(self.login_url + 'index.php', login_data).read()
        except URLError as e:
            print e
        else:
            graph = opener.open(self.graph_url + '?graphid=%s'% (graphid)).read()
            with open('/srv/salt/' +Stime +'.png', 'a+' ) as f:
                print >> f,graph
                f.close()
        image_name = '%s.png' %Stime
        return image_name


if __name__ == "__main__":
    zabbix = tools()

while 1:
    print "Welcome to use this Zabbix API"
    print "Use one of the following options:"
    print "1. search all host"
    print "2. search host"
    print "3. seaech hostgroup"
    print "4. seaech templated"
    print "5. add host"
    print "6. delete host"
    print "7. get  hostids graph.get"
    input = int(raw_input("\nYour selection >"))
    print input
    if input == 1:
        print "search all hostid and hostname [host_get]"
        print "##########################################"
        zabbix.get_host()
        print "#############"
        break
    if input == 3:
        print "hostgroup OK!!!!!!!!!!"
        print "#######################"
        zabbix.get_hostgroup()
        print "#######################"
        break
    if input == 4:
        print "templated OK!!!!!!!!!!"
        print "#######################"
        zabbix.get_templated()
        print "#######################"
        break
    if input == 5:
        print "add hosts OK!!!!!!!!!!"
        print "#######################"
        zabbix.add_host()
        print "#######################"
        break
    if input == 6:
        print "dele host OK!!!!!!!!!!"
        print "#######################"
        zabbix.del_host()
        print "#######################"
        break
    if input == 7:
        print "get graph.get OK!!!!!!"
        print "#######################"
        graph = zabbix.get_graph()
        graphid = int(raw_input('Please input grapid numbers id: '))
        zabbix.get_graphid(graphid)
        break



