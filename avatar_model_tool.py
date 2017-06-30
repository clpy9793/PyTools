#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-30 09:52:27
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import xlrd
import json
import pandas as pd


def main():
    path = [i for i in os.listdir('.') if '价值投放模型' in i]
    if len(path) != 1:
        print(path)
        return
    path = path[0]
    ret = parse_excel(path)
    print('解析excel完毕, 开始修改avatar.csv\n')
    modify_avatar('avatar.csv', ret)
    input('修改完毕, 确认退出\n')

def parse_excel(path, sheetname='临时副本'):
    '''解析excel文件'''
    ret = {}
    two = []
    df = pd.read_excel(path, sheetname=sheetname)

    for i, v in enumerate(df.ID):
        if not (isinstance(v, str) and v.startswith('AV')):
            continue
        attribute = str(df.Attribute[i])
        grade = str(df.Grade[i])
        rare = str(df.Rare[i])
        if attribute == 'nan' or grade == 'nan' or rare == 'nan':
            two.append(v)
            continue
        if grade == '[]' or rare == '0':
            two.append(v)
            continue
        attribute = json.loads(attribute)
        if attribute.count(0) == len(attribute):
            two.append(v)
            continue
        ret[v] = attribute

    with open('2.txt', 'w') as f:
        f.write("\n\n".join(two))
    return ret
    # print(ret)

def modify_avatar(path, data):
    '''修改csv文件'''
    df = pd.read_csv(path)
    one = []
    three = []
    for i, v in enumerate(df.ID):
        if v not in data:
            one.append(v)
            continue
        else:
            df.Attribute[i] = data[v]
            three.append(v)

    df.to_csv(path, index=False)

    with open('1.txt', 'w') as f:
        f.write('\n\n'.join(one))

    with open('3.txt', 'w') as f:
        f.write("\n\n".join(three))
if __name__ == '__main__':
    main()
