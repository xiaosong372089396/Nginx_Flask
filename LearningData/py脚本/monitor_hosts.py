#! /usr/bin/env python
# encoding: utf8

import time
import re
from monitor import models
from django.db.models import Q

# 触发器的事件等级
priority_type = {
    0: "未分类",
    1: "信息",
    2: "警告",
    3: "一般严重",
    4: "严重",
    5: "灾难",
}


class TimeFormat(object):
    @staticmethod
    def time_stamp_to_std(arg):
        time_format = '%Y-%m-%d %H:%M:%S'
        time_obj = time.localtime(arg)
        std_time = time.strftime(time_format, time_obj)
        return std_time

    @staticmethod
    def std_to_time_stamp(arg):
        time_format = '%Y-%m-%d %H:%M:%S'
        time_obj = time.strptime(arg, time_format)
        time_stamp = time.mktime(time_obj)
        return time_stamp


class SearchHostInfo(object):
    """
    处理用户搜索主机组页面
    """

    def __init__(self, host_name=None, ip_address=None, status=None, issue_time=None, issue_level=None):
        self.host_name = host_name
        self.ip_address = ip_address
        self.status = status
        self.issue_time = issue_time
        self.issue_level = issue_level
        self.search_info = []

    def filter_info(self):
        get_all_hosts = self.get_hosts_by_status_time()
        if get_all_hosts:
            for host in get_all_hosts:
                host_info = self.get_host_info(host)
                self.search_info.append(host_info)
            self.search_info.sort(key=lambda info: info['date'], reverse=True)
        return self.search_info

    def get_host_info(self, host):
        host_info = dict()
        try:
            triggers = self.filter_has_triggered_events_by_host_id(host.hostid).order_by('-lastchange')
        except AttributeError:
            return host_info
        error_msg = ""
        if triggers.count():
            description = triggers.first().description
            error_msg = re.sub('\{.*\}', host.name, description)
            events = self.filter_event_by_trigger_id(triggers.first().triggerid).filter(source=0)
            repeat_count = events.filter(value=1).count()
            ack_count = events.filter(value=1, acknowledged=1).count()
            host_info['confirm'] = "是" if repeat_count == ack_count else "否"
        host_info['hostid'] = host.hostid
        host_info['group'] = self.get_group(host.hostid)
        host_info['hostname'] = host.name
        host_info['ip_address'] = self.get_ip_address(host.hostid)
        host_info['status'] = priority_type.get(triggers.first().priority) if triggers.count() else "ok"
        host_info['date'] = TimeFormat.time_stamp_to_std(triggers.first().lastchange) if triggers.count() else ""
        host_info['detail'] = error_msg
        return host_info

    def get_host_info_by_host_id(self, host_id):
        host = self.filter_host_by_host_id(host_id)
        host_info = self.get_host_info(host)
        # triggers = self.filter_host_triggers_by_host_id(host_id)
        # events = self.filter_events_by_triggers_id(triggers.values('triggerid'))
        # for i in events:
        #     print(i)
        return host_info

    def get_host_graphs_info(self, host_id):
        graphs = self.filter_graphs_by_host_id(host_id)
        graphs_info = []
        for graph_id in graphs:
            graph_info = dict()
            graph_data = self.format_history_data_by_host_id_graph_id(graph_id.graphid)
            graph_info['graph_name'] = graph_id.name
            graph_info['graph_id'] = graph_id.graphid
            graph_info['data'] = graph_data
            graphs_info.append(graph_info)
        return graphs_info

    def get_host_graphs_items(self, host_id):
        """获取主机所有的图形列表"""
        graphs = self.filter_graphs_by_host_id(host_id)
        graphs_info = []
        for graph_id in graphs:
            graph_info = dict()
            graph_info['graph_name'] = graph_id.name
            graph_info['graph_id'] = graph_id.graphid
            graphs_info.append(graph_info)
        return graphs_info

    @staticmethod
    def filter_host_by_host_id(host_id):
        """通过主机ID获取主机"""
        host = models.Hosts.objects.filter(hostid=host_id)
        return host.get() if host.all().count() else None

    def get_hosts_by_host_name(self):
        """获取过滤条件主机名或主机别名的所有主机对象"""
        all_hosts = models.Hosts.objects.filter(~Q(status=3), ~Q(flags=2))
        if self.host_name:
            all_hosts = all_hosts.filter(Q(name__contains=self.host_name) | Q(host__contains=self.host_name))
        return all_hosts

    @staticmethod
    def get_ip_address(host_id):
        """
        通过主机ID获取ip地址
        :param host_id:
        :return:
        """
        ip_obj = models.Interface.objects.filter(hostid=host_id).values('ip')
        return list(map(lambda get: get['ip'], ip_obj))

    @staticmethod
    def get_group(host_id):
        """
        通过主机id获取组名
        :param host_id:
        :return:
        """
        group_id = models.HostsGroups.objects.filter(hostid=host_id).values("groupid")
        groups_obj = models.Groups.objects.filter(groupid__in=group_id).values('name')
        return list(map(lambda get: get['name'], groups_obj))

    def get_hosts_by_interface(self):
        """获取过滤条件IP地址后的主机对象"""
        all_hosts = self.get_hosts_by_host_name()
        if all_hosts and self.ip_address:
            filter_hosts_ip = models.Interface.objects.filter(hostid__in=all_hosts.values('hostid'))
            all_hosts_id = filter_hosts_ip.filter(ip__contains=self.ip_address).values('hostid_id')
            all_hosts = all_hosts.filter(hostid__in=all_hosts_id)
        return all_hosts

    def get_hosts_by_status(self):
        """获取过滤条件主机状态是否可用的主机对象"""
        all_hosts = self.get_hosts_by_interface()
        if all_hosts and self.status:
            all_hosts = all_hosts.filter(available=self.status)
        return all_hosts

    def get_hosts_by_priority(self):
        """通过优先级过滤主机"""
        all_hosts = self.get_hosts_by_status()
        if all_hosts and self.issue_level:
            triggers = self.filter_hosts_triggers_by_hosts_id(all_hosts.values('hostid'))
            filter_triggers_id = triggers.filter(priority=self.issue_level, value=1).values('triggerid')
            all_hosts = self.filter_hosts_by_triggers_id(filter_triggers_id)
        return all_hosts

    def get_hosts_by_status_time(self):
        """通过故障时间过滤主机,如果主机无故障则也返回"""
        all_hosts = self.get_hosts_by_priority()
        if all_hosts and self.issue_time:
            self.issue_time = TimeFormat.std_to_time_stamp(self.issue_time)
            triggers = self.filter_hosts_triggers_by_hosts_id(all_hosts.values('hostid'))
            triggers = triggers.filter(Q(lastchange__gte=self.issue_time, value=1))
            all_hosts = self.filter_hosts_by_triggers_id(triggers.values('triggerid'))
        return all_hosts

    @staticmethod
    def filter_host_items_by_host_id(host_id):
        """通过单台主机id获取主机对items对象"""
        items = models.Items.objects.filter(hostid=host_id)
        return items

    @staticmethod
    def filter_hosts_items_id_by_hosts_id(hosts_id):
        """通过主机列表id获取主机列表监控项"""
        items_id = models.Items.objects.filter(hostid__in=hosts_id).values('itemid')
        return items_id if items_id else []

    @staticmethod
    def filter_hosts_id_by_items_id(items_id):
        """通过主机items ID获取主机列表ID"""
        hosts_id = models.Items.objects.filter(itemid__in=items_id).values('hostid')
        return hosts_id if hosts_id else []

    @staticmethod
    def filter_hosts_triggers_id_by_items_id(items_id):
        """通过items id列表获取triggers id列表"""
        triggers_id = models.Functions.objects.filter(itemid__in=items_id).values('triggerid')
        return triggers_id if triggers_id else []

    @staticmethod
    def filter_hosts_items_id_by_triggers_id(triggers_id):
        """通过主机triggers ID获取主机items ID"""
        items_id = models.Functions.objects.filter(triggerid__in=triggers_id).values('itemid')
        return items_id if items_id else []

    @staticmethod
    def filter_hosts_triggers_by_triggers_id(triggers_id):
        """通过triggers_id获取triggers对象"""
        triggers = models.Triggers.objects.filter(triggerid__in=triggers_id)
        return triggers

    def filter_hosts_triggers_by_items_id(self, items_id):
        """通过itemsID获取triggers对象"""
        triggers_id = self.filter_hosts_triggers_id_by_items_id(items_id)
        triggers = self.filter_hosts_triggers_by_triggers_id(triggers_id)
        return triggers

    def filter_hosts_id_by_triggers_id(self, triggers_id):
        """通过触发器ID列表获取主机ID列表"""
        items_id = self.filter_hosts_items_id_by_triggers_id(triggers_id)
        hosts_id = self.filter_hosts_id_by_items_id(items_id)
        return hosts_id

    def filter_hosts_by_triggers_id(self, triggers_id):
        """通过触发器ID列表获取主机列表对象"""
        hosts_id = self.filter_hosts_id_by_triggers_id(triggers_id)
        hosts = models.Hosts.objects.filter(hostid__in=hosts_id)
        return hosts

    def filter_host_triggers_by_host_id(self, host_id):
        """通过单台主机ID获取触发器对象"""
        items_id = self.filter_host_items_by_host_id(host_id).values('itemid')
        triggers = self.filter_hosts_triggers_by_items_id(items_id)
        return triggers

    def filter_hosts_triggers_by_hosts_id(self, hosts_id):
        """通过主机列表对象ID获取触发器"""
        items_id = self.filter_hosts_items_id_by_hosts_id(hosts_id)
        triggers = self.filter_hosts_triggers_by_items_id(items_id)
        return triggers

    def filter_has_triggered_events_by_host_id(self, host_id):
        """通过主机ID获取被触发的触发器对象"""
        triggers = self.filter_host_triggers_by_host_id(host_id).filter(value=1)
        return triggers

    def filter_events_by_triggers_id(self, triggers_id):
        """通过triggersID获取触发事件列表"""
        events = []
        for trigger_id in triggers_id:
            events.append(self.filter_event_by_trigger_id(trigger_id.get('triggerid')))
        return events

    @staticmethod
    def filter_event_by_trigger_id(trigger_id):
        """通过triggerID获取事件event对象"""
        events = models.Events.objects.filter(objectid=trigger_id)
        return events

    def filter_history_by_item_id(self, item_id):
        """通过itemID获取该item历史数据"""
        item = self.filter_item_by_item_id(item_id)
        value_type = item.first().value_type
        history_type = "filter_history_with_type_{}_by_item_id".format(value_type)
        if hasattr(self, history_type):
            history = getattr(self, history_type)
            return history(item_id)
        return dict()

    @staticmethod
    def filter_history_with_type_0_by_item_id(item_id):
        """通过item ID获取valueType=0的数据"""
        history = models.History.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_history_with_type_1_by_item_id(item_id):
        """通过item ID获取valueType=1的数据"""
        history = models.HistoryStr.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_history_with_type_2_by_item_id(item_id):
        """通过item ID获取valueType=2的数据"""
        history = models.HistoryLog.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_history_with_type_3_by_item_id(item_id):
        """通过item ID获取valueType=3的数据"""
        history = models.HistoryUint.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_history_with_type_4_by_item_id(item_id):
        """通过item ID获取valueType=4的数据"""
        history = models.HistoryText.objects.filter(itemid=item_id)
        return history

    @staticmethod
    def filter_item_by_item_id(item_id):
        """通过item ID获取item对象"""
        item = models.Items.objects.filter(itemid=item_id)
        return item

    def format_item_name_by_item_id(self, item_id):
        """
        通过item ID获取对应的监控项名称
        :param item_id:
        :return: 格式化名称返回
        """
        item = self.filter_item_by_item_id(item_id)
        item_name = item.first().name
        item_key = item.first().key_field
        match_str = re.findall('\$\d', item_name)
        try:
            if match_str:
                for position in match_str:
                    index = str(position).lstrip('$')
                    key = re.search('\[.*\]', item_key)
                    key = str(key.group()).strip('[]').split(',') if key else []
                    item_name = re.sub('\$\d', key[int(index)-1], item_name, count=match_str.index(position) + 1)
        except IndexError:
            pass
        return item_name

    def filter_history_by_items_id(self, items_id):
        """
        通过itemsID获取每个item对应的历史数据
        :param items_id: 需要是一个列表格式的字典元素数据
        :return:
        """
        history = []
        for item_id in items_id:
            if type(item_id) is dict:
                item_id = item_id.get('itemid')
            history.append(self.filter_history_by_item_id(item_id))
        return history

    def filter_host_history_by_host_id(self, host_id):
        """通过hostID获取主机监控项历史数据"""
        items_id = self.filter_host_items_by_host_id(host_id).values('itemid')
        history = self.filter_history_by_items_id(items_id)
        return history

    @staticmethod
    def filter_graphs_id_by_items_id(items_id):
        """通过itemsID获取所有相关的graphID"""
        graphs_id = models.GraphsItems.objects.filter(itemid__in=items_id).values('graphid').distinct()
        return graphs_id

    def filter_graphs_by_host_id(self, host_id):
        """通过主机ID获取该主机对应的所有图形"""
        items_id = self.filter_host_items_by_host_id(host_id).values('itemid')
        graphs_id = self.filter_graphs_id_by_items_id(items_id)
        graphs = self.filter_graphs_by_graphs_id(graphs_id)
        return graphs

    @staticmethod
    def filter_graphs_by_graphs_id(graphs_id):
        """通过graphID列表获取graph对象"""
        graphs = models.Graphs.objects.filter(Q(graphid__in=graphs_id) & ~Q(flags=2))
        return graphs

    @staticmethod
    def filter_graph_items_id_by_graph_id(graph_id):
        """通过graphID获取对应的itemsID列表"""
        items_id = models.GraphsItems.objects.filter(graphid=graph_id).values('itemid')
        return items_id

    def filter_graph_items_id_by_graphs_id(self, graphs_id):
        """通过graphsID获取列表形式的{graph_id：items}列表"""
        items_id = []
        for graph_id in graphs_id:
            if type(graph_id) is dict:
                graph_id = graph_id.get('graphid')
            item_id = self.filter_graph_items_id_by_graph_id(graph_id)
            items_id.append({graph_id: item_id})
        return items_id

    def format_history_data_by_host_id_graph_id(self, graph_id):
        """通过graphID获取该图形数据
        :return [{'date':[], 'values': []}]
        """
        graph_data = []
        if type(graph_id) is dict:
            graph_id = graph_id.get('graphid')
        items_id = self.filter_graph_items_id_by_graph_id(graph_id)
        for item_id in items_id:
            item_data = dict()
            if type(item_id) is dict:
                item_id = item_id.get('itemid')
            item_name = self.format_item_name_by_item_id(item_id)
            item_data['item_name'] = item_name
            history = self.filter_history_by_item_id(item_id)
            if history:
                date = list(map(lambda get: "'" + TimeFormat.time_stamp_to_std(get['clock']) + "'", history.values('clock')))
                values = list(map(lambda get: str(get['value']), history.values('value')))
                item_data['date'] = date
                item_data['values'] = values
                graph_data.append(item_data)
        return graph_data
