#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-26 11:44:12
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from __future__ import print_function
import os
import click
import psutil

from subprocess import *
WORKSPACE_PATH = '/workspace'
START_ORDER = ['log', 'center', 'account', 'login', 'game', 'im', 'battle', 'gateway']
STOP_ORDER = ['log', 'center', 'account', 'login', 'game', 'im', 'battle', 'gateway'][::-1]

# 命令组


@click.group()
def manager():
    pass

# 启动
@click.command()
@click.option('--name', help='server name')
@click.option('--count', default=1, help='process count')
def start(name, count):
    if not name:
        start_by_order()
        exit()
    else:
        pass


# 关闭
@click.command()
@click.option('--name', help='server name')
@click.option('--count', default=1, help='process count')
def stop(name, count):
    if not name:
        stop_by_order()
        exit()
    else:
        stop_server(name)


# 重启
@click.command()
@click.option('--name', help='server name')
def restart(name):
    if not name:
        print('restart')
        stop_by_order()
        start_by_order()
    else:
        print('pass')
        pass

manager.add_command(start)
manager.add_command(stop)
manager.add_command(restart)


def start_by_order():
    '''
    按顺序启动服务器
    '''
    for i in START_ORDER:
        start_server(i)
        print('start %s_server' % i)

def stop_by_order():
    '''
    按顺序关闭服务器
    '''
    for i in STOP_ORDER:
        if not i:
            continue
        stop_server(i)
        print('stop %s' % i)


def start_server(name, count=1):
    '''
    根据名字启动相应的服务器
    '''
    cmd = 'twistd -r poll --pidfile {}.pid -l ../../../log/debug/{}.log --umask=022 -y /workspace/newServer/{}_server/src/main.py'.format(name, name, name)
    # print(cmd)
    for i in range(count):
        os.system(cmd)
        pass


def stop_server(name, count=1):
    """根据名字杀掉相关的进程"""
    pids = []
    for pid in psutil.pids():
        try:
            # 遍历所有进程
            p = psutil.Process(pid)
            cmd = p.cmdline()
            # 过滤出所有由Python启动的脚本
            if len(cmd) < 7 or 'python' not in cmd[0]:
                continue
            # cmdline = " ".join(cmd)
            # if name not in cmdline:
            #     continue
            path = cmd[-1]
            # print(1)
            # 根据根目录过滤
            if not path.startswith(WORKSPACE_PATH):
                continue

            # 根据名字过滤
            for x in path.split('/'):
                if x == "{}_server".format(name):
                    break
            else:
                continue
            # print(path)
            pids.append(pid)
        except psutil.NoSuchProcess:
            pass
    if len(pids) < count and count != 0:
        return 
    kill_process(pids, count)


def kill_process(pids, count):
    '''杀死进程'''
    if count == 0:
        count = len(pids)
    for i in range(count):
        os.system('kill -9 %s' % pids[i])


if __name__ == '__main__':
    manager()
