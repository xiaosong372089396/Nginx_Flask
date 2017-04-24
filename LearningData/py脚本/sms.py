#!/usr/bin/env python
#_*_coding:utf-8_*_
import requests
import hashlib
import sys
def sms(validate,tel):
    url = 'http://111111/serverSendMsg'
    mi = '123.com'
    hash=hashlib.md5()
    hash.update(('123,456'+cst_id+validate+mi).encode('utf-8'))
    sign=hash.hexdigest()
    payload = {'cst_id':'1001','sign':sign,'tel':tel,'validate':validate}
    ret = requests.post(url,data=payload)
    print(ret.is_redirect)
    print(ret.text)
    return  ret.text
if __name__ == '__main__':
    tel = sys.argv[1]
    validate = sys.argv[2]
    sms(tel,validate)
