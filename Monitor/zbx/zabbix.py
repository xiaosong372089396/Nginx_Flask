#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import urllib2
import logging

LEVELS = {'debug':logging.DEBUG,
          'info':logging.INFO,
          'warning':logging.WARNING,
          'error':logging.ERROR,
          'critical':logging.CRITICAL,
         }
LOG_FILE = '/srv/salt/API.out'
logging.basicConfig(filename=LOG_FILE, level=LEVELS['info'])

zabbix_url = 'http://192.168.10.87:8088/zabbix/api_jsonrpc.php'
zabbix_user = 'Admin'
zabbix_pawd = '372089396'
header = {"Content-Type":"application/json"}

def auth(url):
    pre_data = {
        "jsonrpc" : "2.0",
        "method" : "user.login",
        "params" : {
                 "user" : zabbix_user,
                 "password" : zabbix_pawd
             },
    "auth": None,
        "id" : 0
    }

    json_data = json.dumps(pre_data)
    request = urllib2.Request(zabbix_url,json_data, header)
    response = urllib2.urlopen(request)
    html =  response.read()
    html_json = json.loads(html)
    return html_json['result']


def get_data(data,hostip=""):
    authid = auth(zabbix_url)
    request = urllib2.Request(zabbix_url,data,header)
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
    #request = urllib2.Request(zabbix_url,data)
    #for key in header:
    #    request.add_header(key,header[key]) 
    #try:
    #    result = urllib2.urlopen(request)
    #except URLError as e:
    #    if hasattr(e, 'reason'):
    #        print 'We failed to reach a server.'
    #        print 'Reason:', e.reason
    #    elif hasattr(e, 'code'):
    #        print 'The server could not fulfill the request.'
    #        print 'Error code: ', e.code
    #    return 0
    #else:
    #    response = json.loads(result.read())
    #    result.close()
    #    return response  

def get_host():
    print "********************************"
    authid = auth(zabbix_url)
    print "authid: " + authid
    data = {
            "jsonrpc":"2.0",
            "method":"host.get",
            "params": {
                    "output" : ["hostid","name"],
                    "filter" : {
                             "host" : ""           
                    },
             },
         "auth":authid,
         "id": 1
    }
    json_data = json.dumps(data)
    print "#################################"
    request = urllib2.Request(zabbix_url,json_data,header)
    response = urllib2.urlopen(request)
    html = response.read()
    html_json = json.loads(html)
    res = html_json['result']
    for host in res:
        print "\t","hostid:",host['hostid'],"\t","host_name:",host['name'].encode('UTF8')

def get_hostgroup():
    authid = auth(zabbix_url)
    data = json.dumps (
          {
             "jsonrpc": "2.0",
             "method": "hostgroup.get",
             "params" : {
             "output" :"extend",
             "filter": {
             }
                      
    },
       "auth": authid,
       "id": 1
    })   
    request = urllib2.Request(zabbix_url,data,header)
    response = urllib2.urlopen(request)
    html = response.read()
    html_json = json.loads(html)
    res =  html_json['result']
    for host in res:
        print "\t","HostGroup_id:",host['groupid'],"\t","HostGroup_name:",host['name'].encode('UTF8')
    
def get_templated():
    print "**********************************"
    authid = auth(zabbix_url)
    data = json.dumps (
           {
              "jsonrpc": "2.0",
              "method" : "template.get",
              "params" : {
                  "output" : "extend",
                  "filter" : {
                  }
    },
         "auth" : authid,
         "id": 1
    })
    request = urllib2.Request(zabbix_url,data,header)
    response = urllib2.urlopen(request)
    html = response.read()
    html_json = json.loads(html)
    res = html_json['result']
    for host in res:
        print "\t","Templateid:",host['templateid'],"\t","Template_name:",host['name'].encode('UTF8')

def add_host():
    print "***********************************"
    authid = auth(zabbix_url)
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
              "auth": authid,
              "id" : 6
        })
    res = get_data(data)
    print "添加主机 : \033[40m%s\031[0m \tid :\033[31m%s\033[0m" % (Hostip, res['result']['hostids'])


def del_host():
    authid = auth(zabbix_url)
    hostip = get_host()
    print hostip
    Hostid = str(raw_input("Please Enter the delete id:"))
    data = json.dumps(
        {
            "jsonrpc":"2.0",
            "method":"host.delete",
            "params": [
                 Hostid
             ],
            "auth":authid,
            "id" :1
    })
    res = get_data(data)
    print "删除主机: \033[40m%s\031[0m \tid :\033[31m%s\033[0m" % (Hostid, res['result']['hostids'])


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
        get_host()
        print "#############"
        break
    if input == 3:
        print "hostgroup OK!!!!!!!!!!"
        print "#######################"
        get_hostgroup()
        print "#######################"
        break
    if input == 4:
        print "templated OK!!!!!!!!!!"
        print "#######################"
        get_templated()
        print "#######################"
        break
    if input == 5:
        print "add hosts OK!!!!!!!!!!"
        print "#######################"
        add_host()
        print "#######################"
        break
    if input == 6:
        print "dele host OK!!!!!!!!!!"
        print "#######################"
        del_host()
        print "#######################"
        break

if __name__ == "__main__":
    log = logging.getLogger('APIlog')
    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')


