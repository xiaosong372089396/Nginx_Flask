#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import urllib2
from urllib2 import URLError
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import ssl
ssl._create_default_https_context=ssl._create_unverified_context


logger = logging.getLogger(__name__)

class tools(object):
    
    def __init__(self):    
        self.zabbix_url = 'http://192.168.10.87:8088/zabbix/api_jsonrpc.php'
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
        return res
#        for host in res:
#            print "\t","hostid:",host['hostid'],"\t","host_name:",host['name'].encode('UTF8')

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
        return res
#            return "\t","HostGroup_id:",host['groupid'],"\t","HostGroup_name:",host['name'].encode('UTF8')


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
        return res
        #for host in res:
        #    print "\t","Templateid:",host['templateid'],"\t","Template_name:",host['name'].encode('UTF8')

    def add_host(self, HostName,Hostip, Groupid,Templateid ):
        print "***********************************"
        # 为测试调用拓展系统 暂且注释 #
        #HostName = str(raw_input("Please input you HostName:"))
        #Hostip = str(raw_input("\033[1;35;40m%s\033[0m" % 'Please Enter your:host_ip :'))
        #Groupid = str(raw_input("\033[1;35;40m%s\033[0m" % 'Please Enter your:group_id :'))
        #Templateid = str(raw_input("\033[1;35;40m%s\033[0m" % 'Please Enter your:template_id :'))
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
        return res
#        return "添加主机 : \033[40m%s\031[0m \tid :\033[31m%s\033[0m" % (Hostip, res['result']['hostids'])


    def del_host(self, id):
#        hostip = self.get_host()
#        print hostip
#        Hostid = str(raw_input("Please Enter the delete id:"))
        Hostid = str(id)
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
        return res
#        print "删除主机: \033[40m%s\031[0m \tid :\033[31m%s\033[0m" % (Hostid, res['result']['hostids'])


'''
if __name__ == "__main__":
    #logger.basicConfig(level=logging.error)
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
'''



