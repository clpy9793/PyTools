#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv
import time
import traceback

DATE_FORMAT = ' %Y-%m-%d %H:%M:%S'
OLD_FILE_PATH = 'new_store.csv'
NEW_FILE_PATH = 'store.csv'


def read_csv():
    _list = []
    with open(OLD_FILE_PATH,'rb') as csv_file:
        r = csv.reader(csv_file)
        _list.append(r.next())
        lst = r.next()
        start = lst.index('StartTime')
        end = lst.index('EndTime')
        _list.append(lst)

        row = 2
        for i in r:
            _list.append(i)
            start_time = i[start]
            end_time = i[end]        
            _list[row][start] = date_2_stamp(start_time)
            _list[row][end] = date_2_stamp(end_time)
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

def date_2_stamp(date):
    try:
        t = time.strptime(date, DATE_FORMAT)
        return int(time.mktime(t))
    except:
        return date



if __name__ == '__main__':
    try:
        data = read_csv()
        write_csv(data)        
        print u'按任意键关闭'
        raw_input()        
    except IOError:                
        print u'请关闭new_store.csv文件,再运行此程序'
        print u'按任意键关闭'
        raw_input()




