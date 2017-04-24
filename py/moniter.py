#encoding: utf-8
import logging
import time

import psutil
import requests

logger = logging.getLogger(__name__)

server_uri = 'http://localhost:9004/moniters/'
def get_local_ip():
    for _net in psutil.net_if_addrs().get('eth0'):
        if _net.family == 2:
            return _net.address
    return None

def moniter_mem():
    path = '/proc/meminfo'
    handler = open(path, 'r')
    total = handler.readline()
    total_list = total.split(' ')
    total_mem = int(total_list[-2])
    free_mem = int(handler.readline().split(' ')[-2])
    buffer_mem = int(handler.readline().split(' ')[-2])
    cached_mem = int(handler.readline().split(' ')[-2])
    logger.debug('%s, %s, %s, %s', total_mem, free_mem, buffer_mem, cached_mem)
    handler.close()
    return 1 - 1.0 * (free_mem + buffer_mem + cached_mem) / total_mem


def moniter_mem2():
    m = psutil.virtual_memory()
    return m.percent

def moniter_cpu():
    return psutil.cpu_percent(interval=1)

def send_to_server(ip, cpu_percent, mem_percent):
    data={'ip' : ip, 'mtime' : int(time.time()), 'cpu' : cpu_percent, 'mem' : mem_percent}
    rt = requests.post(server_uri, data=data)
    logger.debug('%s, %s', str(data), rt.text)

if __name__ == '__main__':
   logging.basicConfig(level=logging.DEBUG)
   ip = get_local_ip()
   while 1:
       mem_percent = moniter_mem2()
       cpu_percent = moniter_cpu()
       send_to_server(ip, mem_percent, cpu_percent)
       time.sleep(60)
