#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-29 15:19:30
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
# from subprocess import *

# jar -uf GA-release-signed.apk ./assets/res/raw-assets/resources/csv
# keytool -genkey -alias ad123.keystore -keyalg RSA -validity 20000 -keystore ad123.keystore
# jarsigner -verbose -keystore ad123.keystore -signedjar GA-release-signed.apk GA-release-signed.apk ad123
jar_cmd = 'jar -uf GA-release-signed.apk ./assets/res/raw-assets/resources/csv'
sign_cmd = 'jarsigner -verbose -keystore ad123.keystore -signedjar GA-release-signed.apk GA-release-signed.apk ad123.keystore'


def main():
    # p = Popen(sign_cmd, stdin=PIPE, stdout=PIPE)
    # p = Popen(['python', '/workspace/manager.py', 'restart'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # print(p.stdout.read().decode())
    # p.stdin.write('123456'.encode())
    os.system(jar_cmd)
    os.system(sign_cmd)
    for i in os.listdir('.'):
        if i.endswith('tmp'):
            os.remove(i)
    # print(p.stdout.read().decode())
    exit()

if __name__ == '__main__':
    main()
