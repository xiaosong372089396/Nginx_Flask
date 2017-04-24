#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, redirect, render_template, session, url_for
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import models
import json
import math

# session 验证
from functools import wraps

sys.path.append("..")
import gconf

Zabbix = Blueprint('zabbix', __name__, url_prefix='/zabbix', template_folder='templates', static_folder='static')


def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args, **kwargs)
        return rtn
    return wapper


# Zabbix API集成
@Zabbix.route('/moniter/',methods=['GET', 'POST'])
@login_required
def monter():
    import zabbix_API
    api = zabbix_API.tools()
    # 组信息
    group_id_list = []
    group_name = []
# 模板信息
    template_id_list = []
    template_name = []
# 获取主机属性
    if request.method == 'GET':
        # 获取 hostgroup信息
        groups = api.get_hostgroup()
        # 获取 template信息
        templates = api.get_templated()
        # 获取zabbix 数据库主机数据
#        hostvalue = models.zabbix_get()
        for host in groups:
            group_id_list.append(host['groupid'].encode('UTF8'))
            group_name.append(host['name'].encode('UTF8'))
            group = dict(zip(group_id_list,group_name))
# 模板信息处理显示
        for template in templates:
            template_id_list.append(template['templateid'].encode('UTF8'))
            template_name.append(template['name'].encode('UTF8'))
            template = dict(zip(template_id_list,template_name))
        return render_template('moniter.html',group=group,template=template)  #  hostid=hostvalue


###############
#zabbix Ajax 添加：
@Zabbix.route('/add_moniter/', methods=['GET','POST'])
@login_required
def add_moniter():
    import zabbix_API
    api = zabbix_API.tools()
    host = []
    id = []
    if request.method == 'POST':
        hostname = request.form.get('hostname')
        ip = request.form.get('ip')
        group_id = request.form.get('group_id')
        g_id = str(group_id[0])
        template_id = request.form.get('template_id')
        t_id = str(template_id[0:5])
        result = api.add_host(hostname,ip,g_id, t_id)
        return "host: %s, id:%s" % (ip, result['result']['hostids'])


################
#zabbix Ajax 删除:
@Zabbix.route('/dele_moniter/',methods=['GET','POST'])
@login_required
def dele_moniter():
    import zabbix_API
    api = zabbix_API.tools()
    if request.method == 'POST':
        hostid = request.form.get('id')
        result = api.del_host(hostid)
        ok = True
        return json.dumps({ 'ok':ok, 'hostid': hostid, 'result': result['result']['hostids'] })
    else:
        #return redirect('/')
        return redirect(url_for('login.log'))


#统计zabbix数据库offset,limit
@Zabbix.route('/zabbix_moniter/',methods=['GET','POST'])
@login_required
def zabbix_moniter():
    # 获取总共次数
    _cnt = models.get_zabbix_count()
    # 获取总共次数向上取整 / 每页显示数量，计算总共可以有多少页
    _max_page_num = int(math.ceil(_cnt * 1.0 / gconf.PAGE_SIZE))
    # 无论是GET,POST请求 都去处理
    params = request.args if request.method == 'GET' else request.form
    #######分页信息,获取点击页数，如果为None,则默认为1
    _page_num = params.get('pageNum', 1)
    # 获取每页显示数量
    _limit = params.get('pageSize', gconf.PAGE_SIZE)
    # 判断页数方法检测字符串是否只由数字组成
    if str(_page_num).isdigit():
        _page_num = int(_page_num)
    else:
        _page_num = 1
    # 判断点击页数是否小于等于0，如果是默认显示到第一页，否则跟着页数走
    if _page_num <= 0:
        _page_num = 1
    else:
        _page_num = _page_num
    # 判断点击页数是否大于最大页数，如果是当前页数等于最大页数，否则当前页数等于当前页数
    if _page_num > _max_page_num:
        _page_num = _max_page_num
    else:
        _page_num = _page_num
    # 如果-1, 意思就是从0开始，   如果不减 第一页就是1 * num, * 每一页显示数量
    _offset = (_page_num - 1) * gconf.PAGE_SIZE
    #####sql = "select * from asset limit %s, %s" % (_offset, _limit)
    #####每页显示数量 5
    if str(_limit).isdigit():
        _limit = _limit
    else:
        _limit = gconf.PAGE_SIZE
    # _offset是第一页，  _limit每页显示数量
    zabbixhost = models.get_zabbix_host(_offset, _limit)
    # 计算开始 0
    if _page_num - 2 > 0:
        _start_page_num = _page_num
    else:
        _start_page_num = 1
    # 计算结束end
    if _start_page_num + 4 > _max_page_num:
        _end_page_num = _max_page_num
    else:
        _end_page_num = _start_page_num
    return render_template('zabbixmoniter.html', hostid=zabbixhost, pageSize=gconf.PAGE_SIZE, pageNum=_page_num,maxPageNum=_max_page_num, startPageNum=_start_page_num, endPageNum=_end_page_num)



























