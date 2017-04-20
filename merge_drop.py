#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-20 17:12:58
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import os
import time
import traceback
import pandas as pd
from inspect import isfunction


class CSVRender(object):
    """CSV解析工具, 用于格式化检查, 依赖pandas"""

    def __init__(self, csv_file=None):
        if csv_file is not None:
            self.df = pd.read_csv(csv_file)

    def read_csv(self):
        pass

    def get_csv_files(self):
        '''读取当前目录的csv文件'''
        self.paths = [i for i in os.listdir('.') if i.endswith('.csv')]

    def for_each_get(self, column='Drop', ignroe='drop.csv'):
        '''遍历文件, 整合数据'''
        for file_name in self.paths:
            if file_name == ignroe:
                continue
            df = pd.read_csv(os.path.abspath(file_name))
            yield os.path.splitext(file_name)[0], list(df[column])

    def update_orign_file(self):
        ''''''
        df = pd.read_csv('drop.csv')
        id_to_index = {v: i for i, v in enumerate(df.Id)}
        for k, v in self.for_each_get():
            if k in id_to_index:
                n = id_to_index[k]
                df.Items.ix[n] = v
            else:
                d = {
                    'Id': os.path.splitext(k)[0],
                    "Items": v,
                    "Type": 0,
                    "Count": []
                }
                df = df.append(d, ignore_index=True)
        df.to_csv('new_drop.csv', index=False)

    @staticmethod
    def check_column(csv_file, column, fn):
        if not isfunction(fn):
            return False
        pd.read_csv(csv_file)
        pass


if __name__ == '__main__':
    try:
        render = CSVRender()
        render.get_csv_files()
        render.update_orign_file()
    except Exception:
        traceback.print_exc()
        time.sleep(3)
