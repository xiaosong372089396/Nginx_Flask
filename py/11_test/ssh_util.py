#encoding:utf-8

import paramiko
import logging
import traceback
import argparse
import getpass

logger = logging.getLogger(__name__)

def ssh_connect(ip, port, user, pwd, commands=[]):
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, pwd)
        for cmd in commands:
            logger.info('exec %s', cmd)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            logger.info('result:%s', stdout.readlines())
    except BaseException as e:
        logger.error('connnect ssh error - %s:%s', ip, port)
        logger.error(traceback.format_exc())

    finally:
        if ssh is not None:
            ssh.close()

if __name__ == '__main__':
     logging.basicConfig(level=logging.INFO)
     parse = argparse.ArgumentParser()
     parse.add_argument('-H', '--host', help='host ip addr', type=str)
     parse.add_argument('-P', '--port', help='host port', type=int)       
     parse.add_argument('-u', '--user', help='host user', type=str)
     parse.add_argument('-c', '--cmd', help='command', type=str, nargs='+')
     args = parse.parse_args()
     if args.host is None or \
        args.port is None or \
        args.user is None or \
        args.cmd is None:
        parse.print_help()
     else:
        pwd = getpass.getpass('请输入密码')
        ssh_connect(args.host, args.port, args.user, pwd, args.cmd)


