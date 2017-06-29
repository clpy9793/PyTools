#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-29 15:58:33
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from __future__ import print_function
import os
import time
from collections import defaultdict
try:
    import ujson as json
except ImportError:
    import json

LOG_LIST = (
    'gateway.log',
    'account.log',
    'game.log',
    'im.log',
    'battle.log',
    'login.log',
)

PATH = '../log/debug/gateway.log'
DATE_FMT = '%Y-%m-%d %H:%M:%S%z'

def filter_input_log(path):
    '''读取日志, 过滤数据'''
    ret = defaultdict(list)
    with open(path, 'r', encoding='utf8', errors='ignore') as f:
        for line in f:
            text = line.split(' ')
            if len(text) <= 5 or text[3] not in {'handle', 'func', 'section'}:
                continue
            ts = " ".join(text[:2])
            ts = time.mktime(time.strptime(ts, DATE_FMT))
            name, cost = text[4:6]
            cost = cost.strip('\n')
            record = (ts, name, cost)
            ret[text[3]].append(record)
    return ret

def each_log():
    '''遍历所有日志'''
    ret = {}
    for log_file in LOG_LIST:
        path = '../log/debug/%s' % log_file
        try:
            server = os.path.splitext(log_file)[0]
            ret[server] = filter_input_log(path)
        except Exception:
            print(path)
            import traceback
            traceback.print_exc()
    return ret


def main():
    ret = each_log()
    with open('parse_result.json', 'w') as f:
        json.dump(ret, f)
    print ('over.')

if __name__ == '__main__':
    main()                