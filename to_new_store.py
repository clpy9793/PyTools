#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import time

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
FILE_PATH = 'store.csv'
NEW_FILE_PATH = 'new_store.csv'


def read_csv():
    _list = []
    with open(FILE_PATH,'rb') as csv_file:
        r = csv.reader(csv_file)
        _list.append(r.next())
        lst = r.next()
        start = lst.index('StartTime')
        end = lst.index('EndTime')
        _list.append(lst)

        row = 2
        for i in r:
            _list.append(i)
            start_time = int(i[start])
            end_time = int(i[end])
            if start_time and end_time:
                _list[row][start] = stamp_2_date(start_time)
                _list[row][end] = stamp_2_date(end_time)
            row+=1
    return _list

def write_csv(data):
    with open(NEW_FILE_PATH,'wb') as csv_file:
        r = csv.writer(csv_file)
        for i in data:
            r.writerow(i)
    return True
            
def stamp_2_date(stamp):
    t = time.localtime(stamp)
    t = r" "+time.strftime(DATE_FORMAT,t)
    return t


if __name__ == '__main__':
    try:
        data = read_csv()
        write_csv(data)        
        print u'按任意键关闭'
        raw_input()        
    except IOError:
        print u'请关闭store.csv文件,再运行此程序'
        print u'按任意键关闭'
        raw_input()




