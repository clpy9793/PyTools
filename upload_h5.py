#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-25 09:35:05
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import shutil
import filecmp
import traceback
from subprocess import check_output

# SRC = r'F:\Battle\client\build\web-mobile'
# DST = r'C:\Users\Administrator\Desktop\tools\tools\h5'
# GZIP_EXE_PATH = r'C:\Users\Administrator\Desktop\tools\tools\gzipall.py'
# UPLOAD_EXE_PATH = r'C:\Users\Administrator\Desktop\tools\tools\upload2oss.py'

SRC = r'C:\Users\lincm.lincm-home\Desktop\web-mobile'
DST = r'F:\Battle\tools\h5'
GZIP_EXE_PATH = r'F:\\Battle\\tools\\gzipall.py'
UPLOAD_EXE_PATH = r'F:\Battle\tools\upload2oss.py'


def commond():
    gzip = 'python {0}'.format(GZIP_EXE_PATH)
    upload = 'python {0}'.format(UPLOAD_EXE_PATH)
    if not os.path.exists(GZIP_EXE_PATH):
        print(u'不存在gzip路径')
    if not os.path.exists(UPLOAD_EXE_PATH):
        print(u'不存在upload2oss路径')
    os.system(gzip)
    os.system(upload)
    # r = check_output(['python', GZIP_EXE_PATH])
    # print('gzip:\n', r)
    # r = check_output([upload])
    # print('upload:\n')
    # for i in r:
    #     print(i)
    print('over')


def main():
    try:
        if os.path.exists(DST):
            print(u'删除目录中...')
            shutil.rmtree(DST)
        print(u'拷贝目录中...')
        shutil.copytree(SRC, DST)
        commond()
    except Exception:
        traceback.print_exc()
    finally:
        input('\npress any key to exit.\n')
if __name__ == '__main__':
    main()
