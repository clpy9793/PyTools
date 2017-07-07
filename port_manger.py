#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-06 11:24:34
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from __future__ import print_function
import os
import re
import random
from subprocess import check_output


class PortManager(object):

    def __init__(self, ignore=None):
        if ignore is None:
            self.ignore = set([])
        else:
            self.ignore = ignore

    def get_random_port(self, nums=1, start=20000, end=30000, step=1, ignore=None):
        used = self.get_used_port(ignore=ignore)
        rst = [i for i in range(start, end, step) if i not in used]
        random.shuffle(rst)
        if nums == 1:
            self.add_ignore([rst[0]])
            return rst[0]
        else:
            self.add_ignore(rst[:nums])
            return rst[:nums]

    def get_used_port(self, ignore=None):
        if ignore is None:
            ignore = set([])
        else:
            ignore = set(ignore)
        r = check_output(['netstat', '-ano'])
        rst = re.findall(r'\d+.\d+.\d+.\d+:(\d+) ', r)
        rst = map(lambda x: int(x), rst)
        return set(rst).union(self.ignore).union(ignore)

    def add_ignore(self, seq):
        if isinstance(seq, int):
            self.ignore.add(seq)
        else:
            for i in seq:
                self.ignore.add(int(i))
        return True


pm_object = PortManager()

if __name__ == '__main__':
    p = PortManager()
    r = p.get_random_port(10)
    print(r)
