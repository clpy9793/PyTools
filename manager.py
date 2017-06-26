#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-26 11:44:12
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import click


def check_server_name(name):
    '''
    检查服务器
    '''
    series = []
    return name in series


# 命令组
@click.group()
def manager():
    pass


# 启动
@click.command()
@click.option('--name', default='center', help='server name')
@click.option('--count', default=1, help='process count')
def start(name, count):
    print(name, count)
    pass


# 关闭
@click.command()
@click.option('--name', default='center', help='server name')
@click.option('--count', default=1, help='process count')
def stop(name, count):
    print(name, count)
    pass


# 重启
@click.command()
@click.option('--name', default='tuan', help='server name')
def restart(name):
    pass

manager.add_command(start)
manager.add_command(stop)
manager.add_command(restart)

def start_by_order():
    order = ['center' 'account' 'login' 'game' 'im' 'battle' 'gateway']
    pass

def start_server(name):
    command = 'python ./newServer/{}_server/src/main.py'.format(name)
    os.system(command)

def stop_server(name):
    path = "{}.pid".format(name)
    if not os.path.exists(path):
        return False
    pids = []
    with open(path, 'r') as f:
        pids = [i for i in f]

    for pid in pids:
        pass
    os.system('kill -9 %d' % (pid, ))
if __name__ == '__main__':
    manager()
