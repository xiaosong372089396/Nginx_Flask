#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import session
from flask import request
import json
import math
import sys
reload(sys)
# session 验证
from functools import wraps

import  models

sys.setdefaultencoding('utf-8')
sys.path.append("..")
import gconf


# 第一个assets 只是个名字， 第二个是访问前缀的意思
assets = Blueprint('assets', __name__, url_prefix='/assets', template_folder='templates', static_folder='static')

def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect('/')
        rtn = func(*args, **kwargs)
        return rtn
    return wapper



#资产管理页面
@assets.route('/addasset/', methods=['POST'])
@login_required
def addAsset():
    if request.method == 'POST':
        sn = request.form.get('sn','')
        ip = request.form.get('ip','')
        hostname = request.form.get('hostname','')
        machine_room_id = request.form.get('machine_room','')
        bussiness = request.form.get('bussiness','')
        admin = request.form.get('admin','')
        cpu = request.form.get('cpu','')
        ram = request.form.get('ram','')
        disk = request.form.get('disk','')
        os = request.form.get('os','')
        model = request.form.get('model','')
        purchase_date = request.form.get('purchase_date','')
        vendor = request.form.get('vendor','')
        statusa = request.form.get('statusa', '')
        # 检查用户提交的数据
        if models.add_asset(sn,ip,hostname,machine_room_id,bussiness,admin,cpu,ram,disk,os,model,purchase_date, vendor, statusa):
            ok = True
            result = '添加成功'
            return json.dumps({ 'ok' : ok, 'result': result })
        else:
            ok = False
            result = '添加失败'
            return json.dumps({ 'ok' : ok, 'result' : result })

# 根据资产主键ID删除信息：
@assets.route('/deleteasset/', methods=['GET', 'POST'])
@login_required
def deleteasset():
    if request.method == 'POST':
        _id = request.form.get('id')
        if models.delete_asset(_id):
            ok = True
            result = '删除成功'
            return json.dumps({ 'ok': ok, 'result': result })
        else:
            ok = False
            result = '删除失败'
            return json.dumps({ 'ok': ok, 'result': result })
    return redirect('/user/')


#资产管理修改
@assets.route('/assets_update/', methods=['POST'])
@login_required
def assets_update():
    if request.method == 'POST':
        id = request.form.get('id')
        sn = request.form.get('sn')
        ip = request.form.get('ip')
        hostname = request.form.get('hostname')
        machine_room = request.form.get('machine_room')
        bussiness = request.form.get('bussiness')
        admin = request.form.get('admin')
        cpu = request.form.get('cpu')
        ram = request.form.get('ram')
        disk = request.form.get('disk')
        os = request.form.get('os')
        model = request.form.get('model')
        purchase_date = request.form.get('purchase_date')
        vendor = request.form.get('vendor')
        statusb = request.form.get('statusb')
        if models.assetsupdate(sn, ip, hostname, machine_room, bussiness, admin, cpu, ram, disk, os, model, purchase_date, vendor, statusb, id):
            ok = True
            result = '修改成功'
            return json.dumps({ 'ok' : ok, 'result': result })
        else:
            ok = False
            result = '修改失败'
            return json.dumps({ 'ok' : ok, 'result' : result })


#资产管理页面, 分页
@assets.route('/assets/', methods=['GET','POST'])
@login_required
def asset():
#################这边是显示 从第1页到最后一页相关的参数
    #获取总共次数
    _cnt = models.get_asset_count()
    #获取总共次数向上取整 / 每页显示数量，计算总共可以有多少页
    _max_page_num = int(math.ceil(_cnt * 1.0 / gconf.PAGE_SIZE))
    #无论是GET,POST请求 都去处理
    params = request.args if request.method == 'GET' else request.form
    #获取html传递过来的query次数,
#    _query = params.get('query', '')
#######分页信息,获取点击页数，如果为None,则默认为1
    _page_num = params.get('pageNum', 1)
    #获取每页显示数量
    _limit = params.get('pageSize', gconf.PAGE_SIZE)

    #判断页数方法检测字符串是否只由数字组成
    if str(_page_num).isdigit():
        _page_num = int(_page_num)
    else:
        _page_num = 1
# _page_num = int(_page_num) if str(_page_num).isdigit() else 1
    #判断点击页数是否小于等于0，如果是默认显示到第一页，否则跟着页数走
    if  _page_num <= 0:
        _page_num = 1
    else:
        _page_num = _page_num
# _page_num = 1 if _page_num <= 0 else _page_num

    #判断点击页数是否大于最大页数，如果是当前页数等于最大页数，否则当前页数等于当前页数
    if  _page_num > _max_page_num:
        _page_num = _max_page_num
    else:
        _page_num = _page_num
# _page_num = _max_page_num if _page_num > _max_page_num else _page_num

    #如果-1, 意思就是从0开始，   如果不减 第一页就是1 * num, * 每一页显示数量
    _offset = (_page_num - 1) * gconf.PAGE_SIZE

#####sql = "select * from asset limit %s, %s" % (_offset, _limit)
#####每页显示数量 5
    if  str(_limit).isdigit():
        _limit = _limit
    else:
        _limit = gconf.PAGE_SIZE
# _limit = _limit if str(_limit).isdigit() else gconf.PAGE_SIZE

    # _offset是第一页，  _limit每页显示数量
    _assets = models.get_assets(_offset, _limit)

    # 计算开始 0
    if  _page_num - 2 > 0:
        _start_page_num = _page_num
    else:
        _start_page_num = 1
# _start_page_num = _page_num if _page_num -2 > 0 else 1

    # 计算结束end
    if  _start_page_num + 4 > _max_page_num:
        _end_page_num = _max_page_num
    else:
        _end_page_num = _start_page_num
# _end_page_num = _max_page_num if _start_page_num +4 > _max_page_num else _start_page_num
    return render_template('assets.html', assets=_assets, pageSize=gconf.PAGE_SIZE, pageNum=_page_num, maxPageNum=_max_page_num, startPageNum=_start_page_num, endPageNum=_end_page_num)


#查找
@assets.route('/select/',methods=['GET','POST'])
@login_required
def select():
    if request.method == 'POST':
        username = request.form.get('user')
        data = models.mysql_select(username)
        return render_template('select.html', pages=data)

'''
##查询用户管理
@assets.route('/assetselect/', methods=['GET', 'POST'])
@login_required
def assetselect():
    _assets = []
    _query = ''
    return render_template('assets/assets.html', assets=_assets, query=_query)

###################################  echarts画图
@assets.route('/moniters/', methods=['POST'])
def moniter():
    mtime = request.form.get('mtime', '')
    ip = request.form.get('ip', '')
#strftime函数接收以时间元组，并返回以可读字符串表示的当地时间， 格式由参数format决定
    mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(mtime)))
#localtime函数类似gmtime(),作用是格式化时间戳为本地时间，如果sec参数未输入，则以当前时间为转成标准
    cpu = request.form.get('cpu', '')
    mem = request.form.get('mem', '')
    disk = request.form.get('disk', '')
    rt = models.Moniter(mtime, ip, cpu, mem, disk)
    return json.dumps({'code' : rt })

@assets.route('/moniters/<pk>/', methods=['GET'])
@login_required
def getmoniter(pk=None):
    _data = models.getData(pk)
    return json.dumps({'code' : 200, 'data' : _data})
'''























