# -*- coding: utf-8 -*-
import pycurl
from io import BytesIO
import json
class Handler(object):
    def __init__(self, url, **kwargs):
        self.url = url
        self.header = kwargs.get("header", None)
        self.curl = pycurl.Curl()
        self.curl.setopt(self.curl.URL, self.url)
        self.curl.setopt(self.curl.HEADER, False)
        self.curl.setopt(self.curl.POST, True)
        if self.header:
            self.curl.setopt(self.curl.HTTPHEADER, self.header)

    def request(self, data=None, timeout=None):
        if isinstance(data, str):
            self.curl.setopt(pycurl.POSTFIELDS, data)
        header_buf = BytesIO()
        body_buf = BytesIO()
        self.curl.setopt(self.curl.FRESH_CONNECT, True)
        self.curl.setopt(self.curl.FORBID_REUSE, True)
        if str(timeout).isdigit() and timeout > 0:
            self.curl.setopt(self.curl.TIMEOUT, timeout)
        self.curl.setopt(self.curl.HEADERFUNCTION, header_buf.write)
        self.curl.setopt(self.curl.WRITEFUNCTION, body_buf.write)
        try:
            self.curl.perform()
        except pycurl.error:
            return False
        http_code = self.curl.getinfo(self.curl.HTTP_CODE)
        self.curl.close()
        return {"http_code": http_code, "header": header_buf.getvalue(), "body": body_buf.getvalue(), "url": self.url}
class API(object):

    def __init__(self, url, **kwargs):
        self.timeout = kwargs.get("timeout", 30)
        self.header = kwargs.get("header", ["Content-Type: application/json"])
        self.response = kwargs.get("response", None)
        self.auth_string = kwargs.get("auth_string", None)
        self.url = url

    def post(self, method, task_id=1, auth=None, **params):
        handler = Handler(self.url, header=self.header)
        data = {"jsonrpc": "2.0", "method": method, "params": params, "id": task_id, "auth": auth}
        print(data)
        result = handler.request(data=json.dumps(data), timeout=self.timeout)
        if not result:
            return result
        if result["http_code"] != 200:
            self.response = "response code %s".format(result["info"]["http_code"])
            return self.response
        result = json.loads(result["body"].decode())
        if "error" in result and result["error"]:
            self.response = "%s(%s)" % (result["error"]["data"], result["error"]["code"])
            return self.response
        return result["result"]

    def auth(self, user, password):
        result = self.post("user.login", user=user, password=password, task_id=1)
        if result:
            self.auth_string = result
        return result

    def get_host_group(self, **params):
        return self.post("hostgroup.get", task_id=2, auth=self.auth_string, **params)

    def get_host(self, **params):
        return self.post("host.get", task_id=3, auth=self.auth_string, **params)

    def get_graph(self, **params):
        return self.post("graph.get", task_id=4, auth=self.auth_string, **params)

    def get_item(self, **params):
        return self.post("item.get", task_id=5, auth=self.auth_string, **params)

    def get_trends(self, **params):
        return self.post("trends.get", task_id=6, auth=self.auth_string, **params)

    def get_history(self, **params):
        return self.post("history.get", task_id=7, auth=self.auth_string, **params)
    def host_create(self,**params):
        return self.post("host.create",task_id=1,auth=self.auth_string,**params)
    def template_get(self,**params):
        return self.post("template.get",task_id=1,auth=self.auth_string,**params)
def dic(hostname,ip):
    create = {
        "host":hostname,
        "interfaces":
        [
        {"type": 1,"main": 1,"useip": 1,"ip":ip,"dns": "","port": "10050"}
        ],
       "groups": [{"groupid":"8"}],"templates": [{"templateid": "10144"}]
    }
    return create
if __name__ == '__main__':
    api = API("http://1.1.1.1/api_jsonrpc.php")
    result = api.auth("123.com", "123.com")
    if result:
        result = api.get_host_group(**{"output": "extend"})
        for i in result:
            print(i)
        file = open('host','r+')
        for i in file:
            print(i)
            hostname,ip = i.split(':')[0],i.split(':')[1]
            create = dic(hostname,ip)
            result = api.host_create(**create)
            print(result)
