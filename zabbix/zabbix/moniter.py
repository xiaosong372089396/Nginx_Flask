#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import time

import psutil
import requests

logger = logging.getLogger(__name__)

server_uri = 'http://localhost:5000/moniters/'

def get_local_ip():
    for _net in psutil.net_if_addrs().get('em1'):
        if _net.family == 2:
            return _net.address
        return None

def monitor_cpu():
    cpu = psutil.cpu_percent(interval=1)
    return  cpu

def monitor_mem():
    mem = psutil.virtual_memory()
    return mem.percent

def monitor_disk():
    disk = psutil.disk_usage('/').percent
    return disk 

def send_to_server(ip, cpu_percent, mem_percent, disk_percent):
    data = {'ip' : ip, 'mtime' : int(time.time()), 'cpu' : cpu_percent, 'mem' : mem_percent, 'disk' : disk_percent}
    rt = requests.post(server_uri, data=data)
    logger.error('%s, %s', str(data), rt.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.error)
    ip = get_local_ip()
    while 1:
        cpu_percent = monitor_cpu()
        logger.error('cpu_percent:%s', cpu_percent)
        mem_percent = monitor_mem()
        logger.error('mem_percent:%s', mem_percent)
        disk_percent = monitor_disk()
        logger.error('disk_percent:%s', disk_percent)
        send_to_server(ip, cpu_percent, mem_percent, disk_percent)
        time.sleep(60)




