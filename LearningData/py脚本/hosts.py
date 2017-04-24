#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun 
@date 16/9/7
"""
import time
import re


class TimeConvert:
    @staticmethod
    def unix_time_conv(arg):
        """
        unit_time时间转换成标准时间
        :return:
        """
        time_format = '%Y-%m-%d %H:%M:%S'
        time_obj = time.localtime(arg)
        time_std = time.strftime(time_format, time_obj)
        return time_std

    @staticmethod
    def std_time_conv(arg):
        """
        标准时间转换成unix_time
        :param arg:
        :return:
        """
        time_format = '%Y-%m-%d %H:%M:%S'
        time_obj = time.strptime(arg, time_format)
        time_unix = time.mktime(time_obj)
        return time_unix
print(TimeConvert.unix_time_conv(1473271761))
print(TimeConvert.unix_time_conv(585434788))


class HostInfo(object):
    """
    通过hostid获取主机相关状态
    """

    def __init__(self, host_id):
        self.host_id = host_id

    def get_host_name(self):
        """
        通过host_id获取主机名
        :return:
        """
        host = models.Hosts.objects.get(hostid=self.host_id)
        host_name = host.name
        return host_name

    def get_host_gid(self):
        """
        通过host_id获取主机组id，如果主机从属多个组，则只获取一个所属组id
        :return:
        """
        host_grp = models.HostsGroups.objects.filter(hostid=self.host_id).order_by("groupid").all()
        list_host_grp = []
        for item in host_grp:
            list_host_grp.append(item.groupid_id)
        return list_host_grp

    def get_host_gname(self):
        """
        通过host_gid获取主机组名，由于get_host_gid()方法只获取一个组id
        所以获取的组名也只有一个
        :return:
        """
        host_gid = self.get_host_gid()
        host_gname = models.Groups.objects.filter(groupid__in=host_gid).order_by("name").all()
        list_host_gname = []
        for item in host_gname:
            list_host_gname.append(item.name)
        return list_host_gname

    def get_host_ip(self):
        """
        通过host_id获取主机ip地址
        :return:
        """
        host_ip = models.Interface.objects.get(hostid=self.host_id)
        host_ip = host_ip.ip
        return host_ip

    def get_host_item_id(self):
        """
        通过host_id获取主机所有的监控项目items_id
        :return:
        """
        hst_itm = models.Items.objects.filter(hostid=self.host_id).all()
        list_items_id = []
        for item in hst_itm:
            list_items_id.append(item.itemid)
        host_items_id = list_items_id
        return host_items_id

    def get_host_trigger_id(self):
        """
        通过items_id获取主机所有监控项目已经被定义的triggers_id
        :return:
        """
        host_items_id = self.get_host_item_id()
        hst_tid = models.Functions.objects.filter(itemid__in=host_items_id).all()
        list_trigger_id = []
        for item in hst_tid:
            list_trigger_id.append(item.triggerid_id)
        return list_trigger_id

    def get_host_total_cnt(self):
        """
        通过triggers_id获取主机所有已被触发的triggers的总数
        :return:
        """
        host_triggers_id = self.get_host_trigger_id()
        host_total_cnt = models.Triggers.objects.filter(triggerid__in=host_triggers_id, status=0, value=1).count()
        return host_total_cnt

    def get_host_status(self):
        """
        通过主机被触发的triggers的总数来判断主机是否正常
        :return:
        """
        host_total_cnt = self.get_host_total_cnt()
        if host_total_cnt:
            host_status = '故障'
        else:
            host_status = '正常'
        return host_status

    def get_host_triggers_lastcheck(self):
        """
        获取主机所有已被触发triggers的最新时间，告警级别，告警详细
        :return:
        """
        host_name = self.get_host_name()
        host_triggers_id = self.get_host_trigger_id()
        hst_lastcheck = models.Triggers.objects.filter(triggerid__in=host_triggers_id, status=0, value=1).all()
        list_triggers_lastcheck = []
        dict_level = {1: "灾难", 2: "严重", 3: "一般严重", 4: "警告", 5: "信息"}
        for item in hst_lastcheck:
            if not dict_level.get(item.priority):
                lastcheck_level = "未分类"
            else:
                lastcheck_level = dict_level.get(item.priority)
            description = re.sub(r'\{HOST\.NAME\}', host_name, item.description)
            lastcheck_time = TimeConvert.unix_time_conv(item.lastchange)
            list_triggers_lastcheck.append([description, lastcheck_level, lastcheck_time])
        return list_triggers_lastcheck

    def get_host_ack(self):
        """
        获取主机所有被触发监控的信息是否已被确认，及确认的详细信息
        :return:
        """
        list_trigger_id = self.get_host_trigger_id()
        if list_trigger_id:
            ack_event = models.Events.objects.filter(objectid__in=list_trigger_id, source=0)\
                .order_by("-clock").all()
        list_ack_event = []
        if ack_event:
            for item in ack_event:
                change_time = TimeConvert.unix_time_conv(item.clock)
                ack_status = item.acknowledged
                if item.acknowledged:
                    ack_obj = models.Acknowledges.objects.get(eventid=item.eventid)
                    ack_time = TimeConvert.unix_time_conv(ack_obj.clock)
                    ack_msg = ack_obj.message
                else:
                    ack_time = ''
                    ack_msg = ''
                list_ack_event.append([item.eventid, change_time, ack_status, ack_time, ack_msg])
        return list_ack_event



class SearchHost(object):
    def __init__(self, arg):
        self.host_name = arg.get('host-name', None)
        self.host_ip = arg.get('ip', None)
        self.host_status = arg.get('status', None)
        self.last_change = arg.get('issue-time', None)
        self.warn_level = arg.get('issue-level', None)

    @staticmethod
    def all_host():
        set_all_hosts = set()
        type_host = [1, 2]
        all_hosts_obj = models.Hosts.objects.filter(available__in=type_host).all()
        for item in all_hosts_obj:
            set_all_hosts.add(item.hostid)
        return set_all_hosts

    def search_by_hostname(self):
        """
        通过主机名查询，返回符合条件的hostid列表
        :return:
        """
        li_search_hostname = []
        if self.host_name is not None:
            filter_hostname = models.Hosts.objects.filter(available__in=[1, 2], host__contains=self.host_name).all()
            for item in filter_hostname:
                li_search_hostname.append(item.hostid)
        else:
            filter_hostname = models.Hosts.objects.all()
            for item in filter_hostname:
                li_search_hostname.append(item.hostid)
        return set(li_search_hostname)

    def search_by_ipaddr(self):
        """
        通过主机IP地址查询，返回符合条件的hostid列表
        :return:
        """
        search_ip = []
        if self.host_ip is not None:
            filter_ip = models.Interface.objects.filter(ip__contains=self.host_ip).all()
            for item in filter_ip:
                search_ip.append(item.hostid_id)
        else:
            filter_ip = models.Interface.objects.all()
            for item in filter_ip:
                search_ip.append(item.hostid_id)
        return set(search_ip)

    def search_by_host_status(self):
        """
        通过主机状态查询，返回符合条件的主机列表
        :return:
        """
        normal_host = []
        abnormal_host = []
        all_hosts = SearchHost.all_host()
        if all_hosts:
            for host_id in all_hosts:
                host_obj = HostInfo(host_id)
                if host_obj.get_host_total_cnt():
                    abnormal_host.append(host_id)
                else:
                    normal_host.append(host_id)
        else:
        {"action": "look"}