#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-19 11:04:32
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import sqlite3

db_name = 'wc.db'

def main():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('select * from work_queue;')
    c.execute('delete from work_queue;')
    conn.commit()

if __name__ == '__main__':
    main()
