#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-06 09:13:04
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import time
import types
import poplib
import hashlib
import logging
from functools import wraps
from urllib.parse import unquote
from contextlib import contextmanager
from inspect import signature, isfunction
import pydevd
import requests


class Timer:
    '''具有启动, 暂停, 重置功能的简易计时器'''

    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


@contextmanager
def timeblock(label):
    '''代码块运行时间'''
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print('{} : {}'.format(label, end - start))


def send_mail():
    '''SendCloud发送邮件'''
    url = 'http://api.sendcloud.net/apiv2/mail/send'
    params = {
        "apiUser": "",
        "apiKey": "",
        "from": "",
        "fromName": "GA_ROBOT",
        "to": "",
        "subject": "程序故障",
        "html": "你太棒了！你已成功的从SendCloud发送了一封测试邮件，接下来快登录前台去完善账户信息吧！",
    }
    return requests.post(url, json=params)


@try_again(3)
def q():
    import random
    n = random.randint(1, 3)
    print('xx')
    if n != 1:
        raise TypeError('test')


def try_again(n):
    '''忽略一定次数异常'''
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            times = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if times == n:
                        raise e
                    times += 1
        return wrapper
    return decorate


def give_hello(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('begin {0}'.format(func.__name__))
        result = func(*args, **kwargs)
        print('end {0}'.format(func.__name__))
        return result
    return wrapper


def gen_drop(drop_id, count, can_repeat, exclude_list, DROP):
    import pandas as pd
    rst = []
    drop_list = []
    weights = []
    if exclude_list is None:
        exclude_list = []
    exclude_list = set(exclude_list)
    for item in DROP[drop_id].Items:
        if item['id'] in exclude_list:
            weights.append(0)
        else:
            weights.append(item['rate'])
        drop_list.append(item['id'])

    s = pd.Series(drop_list)
    r = s.sample(count, replace=can_repeat, weights=weights)
    for i, v in enumerate(r):
        if v in DROP:
            rst.extend(
                gen_drop(v, DROP[drop_id].Items[i]['count'],
                         can_repeat, exclude_list, DROP))
        else:
            rst.append(v)
    return rst


@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()


@contextmanager
def time_sign():
    print('{}'.format(time.asctime()))
    yield
    print('\n{}'.format(time.asctime()))


def fun(d):
    return sorted(d.items(), key=lambda x: x)


def gen_shandw_sign(data, key=""):
    """sdw"""
    data = {str(k): v for k, v in data.items()}
    rst = sorted(data.items(), key=lambda x: x[0])
    rst = ["{}={}".format(i[0], i[1])
           for i in rst if (i[0] != 'memo' and i[1])]
    print(rst)
    stringA = "&".join(rst)
    stringSignTemp = "{}{}".format(stringA, key)
    signValue = hashlib.md5(stringSignTemp.encode()).hexdigest().lower()
    return signValue


def get_rank_count():
    """计算当前时间对应的场次"""
    t = time.localtime()
    return t.tm_hour * 2 + int(t.tm_min / 30) + 1


def get_seconds():
    """计算距离指定时间点剩余的时间"""
    t = time.localtime()
    minute = t.tm_min % 30
    return (30 - minute) * 60 - t.tm_sec


class NoMixedCaseMeta(type):
    """拒绝大小写混合的类成员"""

    def __new__(mcs, clsname, bases, clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError('bad attribute name: {}'.format(name))
        return super().__new__(mcs, clsname, bases, clsdict)


class Singleton(type):
    """单例"""

    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Profiled:
    """添加函数调用次数的统计"""

    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self

        return types.MethodType(self, instance)


class Route(dict):
    """路由, 通过函数名访问函数"""

    def __call__(self, f):
        if isfunction(f):
            self[f.__name__] = f
            return f
        else:
            raise TypeError('Route argument must be function')


def typeassert(*ty_args, **ty_kwargs):
    """类型强制检查"""
    def decorate(func):
        if not __debug__:
            return func
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if not isinstance(value, bound_types[name]):
                    raise TypeError('Argument {} must be {}'.format(
                        name, bound_types[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorate


def debugger(func, remote=("192.168.1.178", 13333)):
    """Pycharm快速调试"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ip, port = remote
            pydevd.settrace(ip, port=port, stderrToServer=True,
                            stdoutToServer=True)
            result = func(*args, **kwargs)
            return result
        finally:
            pydevd.stoptrace()
    return wrapper


def see_context(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print('function', func.__name__)
        print('args', args)
        print('kwargs', kwargs)
        print('result', result)
        return result
    return wrapper


def timethis(func):
    """函数消耗时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('{}\t{}'.format(func.__name__, end - start))
        return result
    return wrapper


def unquotedata(data):
    """去URL编码"""
    d = {}
    for k, v in data.items():
        try:
            d[k] = unquote(v)
        except Exception:
            d[k] = v
    return d


def get_mail_list(self):
    email = ''
    password = ''
    pop3_server = ''
    server = poplib.POP3_SSL(pop3_server)
    server.set_debuglevel(1)
    server.user(email)
    server.pass_(password)
    _, mails, _ = server.list()
    msg = "count: {}".format(len(mails))
    logging.info(msg)


if __name__ == '__main__':
    pass
