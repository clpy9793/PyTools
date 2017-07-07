#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-01 10:35:05
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
"""
install environment for centos7.2
"""
from __future__ import print_function
import os

def install_yum():
    os.system("yum -y groupinstall 'Development Tools'")
    os.system("yum -y yum install zlib-devel bzip2-devel  openssl-devel ncurses-deve")
    os.system('yum  -y install readline-devel')

def install_python2():
    os.system('rm Python-2.7.* -rf')
    os.system("yum -y yum install zlib-devel bzip2-devel  openssl-devel ncurses-deve")
    os.system('wget  https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tar.xz')
    os.system('tar Jxvf  Python-2.7.12.tar.xz')
    os.system('cd Python-2.7.12')
    if not os.path.exists('/usr/local/python27'):
        os.system('mkdir /usr/local/python27')

    os.system('./configure --prefix=/usr/local/python27')
    os.system('make && make install')
    os.system("echo 'export PATH=$PATH:/usr/local/python27/bin' >> ~/.bashrc")


def install_python3():
    os.system('rm Python-3.5.* -rf')
    os.system("yum -y yum install zlib-devel bzip2-devel  openssl-devel ncurses-deve")
    os.system('wget  https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz')
    os.system('tar Jxvf  Python-3.5.2.tar.xz')
    os.system('cd Python-3.5.2')
    if not os.path.exists('/usr/local/python35'):
        os.system('mkdir /usr/local/python35')
    os.system('./configure --prefix=/usr/local/python35')
    os.system('make && make install')
    os.system("echo 'export PATH=$PATH:/usr/local/python35/bin' >> ~/.bashrc")

def install_mysql():
    os.system('wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm')
    os.system('rpm -ivh mysql-community-release-el7-5.noarch.rpm')
    os.system('yum -y update')
    os.system('yum -y install mysql-server')

def install_redis():
    pass
    os.system('yum -y install redis python-redis')



def main():
    # os.system('su -')
    # install_yum()
    # install_python2()
    # install_python3()
    # install_mysql()
    install_redis()

if __name__ == '__main__':
    main()
