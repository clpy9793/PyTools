#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-02 20:45:53
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from __future__ import print_function
import os
import time
import requests
import paramiko
import traceback

paramiko.util.log_to_file('ssh.log')

IP = ''
USER = ''
PWD = ''
PORT = 22

DOWNLOAD_PATH = '/workspace/newServer/game_server/data'

REMOTE_DIR = [
    '/workspace/newServer/game_server',
    '/workspace/newServer/im_server',
    '/workspace/newServer/battle_server'
]

def patch_crypto_be_discovery():

    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller freezing.
    """

    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
    ]



def main():
    upload_dir()
    notify_restart()
    # download_dir()
    # restart_server()

def notify_restart():
    url = 'http://114.55.236.30:7979/admin/restart'
    r = requests.get(url)
    if r.text == "Success":
        print(u'重启服务器成功')
        time.sleep(2)
    else:
        print(u'重启失败', r.text)
        time.sleep(3)



def download_dir():
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(IP, PORT, USER, PWD)    
    stdin, stdout, stderr = s.exec_command("ls %{0}".format(DOWNLOAD_PATH))
    print(stdout.read().decode('utf8'))
    # t = paramiko.Transport((IP, PORT))
    # t.connect(username=USER, password=PWD)
    # sftp = paramiko.SFTPClient.from_transport(t)
    # print(u'文件下载中...')



def restart_server():
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(IP, PORT, USER, PWD)

    stdin, stdout, stderr = s.exec_command("bash -l -c 'cd /workspace;python ./restart.py'")
    print(stdout.read(), stderr.read())
    s.close()


def upload_dir():
    t = paramiko.Transport((IP, PORT))
    t.connect(username=USER, password=PWD)
    sftp = paramiko.SFTPClient.from_transport(t)
    print(u'文件上传中...')
    for path in [i for i in os.listdir('.') if i.endswith('csv')]:
        local = "./" + path
        for dirs in REMOTE_DIR:
            remote = "{0}/data/{1}".format(dirs, path)
            upload_file(t, sftp, local, remote)


def upload_file(t, sftp, local, remote):
    print('{0}\t{1}'.format(local, remote))
    sftp.put(local, remote)


if __name__ == '__main__':
    try:
        patch_crypto_be_discovery()
        main()
    except Exception:
        s = traceback.format_exc()
        print(s)
        with open('errors.log', 'w') as f:
            f.write(s)
    finally:
        print(u"任务结束, 即将关闭")
        time.sleep(1)
