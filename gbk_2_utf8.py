#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-30 14:16:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sys
import traceback
reload(sys) 
sys.setdefaultencoding('UTF8')

def main():
    paths = os.listdir('.')
    paths = filter(lambda x:x.endswith('csv'), paths)
    for i in paths:
        func(i)

def func(file_path):
    try:
        lst = []
        lst = read(file_path)
        lst = parse(lst)
        write(lst,file_path)
    except (UnicodeDecodeError,UnicodeEncodeError):
        pass
    except :                
        traceback.print_exc()
        print file_path
        raw_input()


def parse(lst):
    print('parseing')
    lst = map(lambda x:x.decode('gbk').encode('utf8'), lst)
    print('done.')
    return lst

def read(file_path):
    print('reading...')
    lst = []
    with open(file_path,'rb') as f:
        lst = f.readlines()
    print('done.')  
    return lst

def write(lst,file_path):
    print('writing...')   
    with open(file_path, 'wb') as f:
        for s in lst:
            f.write(s)    
    print('done.')
if __name__ == '__main__':
    main()
