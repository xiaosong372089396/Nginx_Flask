#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib,urllib2,json,sys,re
import ssl
reload(sys)
sys.setdefaultencoding('utf-8')
ssl._create_default_https_context=ssl._create_unverified_context

class salt_api(object):
    def __init__(self):
        self.__url =  'https://192.168.10.87:8000'   #api接口地址
        self.__user =  'saltapi'
        self.__password = 'saltapi'
        self._tokenid = self.salt_auth()

    def salt_auth(self):
        params = {'username':self.__url,'username':self.__user, 'password':self.__password, 'eauth': 'pam'}
        encode = urllib.urlencode(params)      #转换成url参数格式 username=saltapi&password=saltapi&eauth=pam
        obj = urllib.unquote(encode)           #转换成encode格式 username=saltapi&password=saltapi&eauth=pam
        headers = {'X-Auth-Token':''}
        url = self.__url + '/login'
        request = urllib2.Request(url,obj,headers)
        response = urllib2.urlopen(request)
        content = json.loads(response.read())
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError

    def salt_prefix(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self._tokenid}
        request = urllib2.Request(url, obj, headers)
        response = urllib2.urlopen(request)
        content = json.loads(response.read())
        return content['return']

    def salt_run(self, params):
        obj = urllib.urlencode(params)
        obj, number = re.subn("arg\d", 'arg', obj)
        res = self.salt_prefix(obj)
        return res

# Ip传过来，IP默认为None
    def main(self, ip=None, fun=None, arg=None):
        #  params = {'client': 'local', 'tgt':ip, 'fun': 'cmd.run', 'arg':'df -Th'}
        #params = {'client' : 'local', 'expr_form': 'pcre', 'tgt': '192.168.10.200',  'fun': 'state.sls', 'arg': 'snmp'}
        params = {'client':  'local', 'expr_form': 'pcre', 'tgt': ip, 'fun': fun, 'arg':arg}
        test = self.salt_run(params)
        return test


#if __name__ == '__main__':
#    a = salt_api()
#    a.main()

#curl -k https://192.168.10.87:8000/login -d username='saltapi' -d password='saltapi' -d eauth='pam' | python -mjson.tool
#curl -k https://192.168.10.87:8000/minions -H "Accept: application/x-yaml" -H "X-Auth-Token:fbe19fd6c0ec274d4cb461d5d73fbcf3b4f1649c"






