#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-20 10:59:32
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import pandas as pd


def main():
    dr_set = set()
    ar_set = set()
    df = pd.read_csv('rabbit.csv')
    lines = []
    for i, v in enumerate(df.dr):
        dr = df.ix[i, 'dr']
        ar = df.ix[i, 'ar']
        if dr in dr_set or ar in ar_set:
            continue

        line = "{} = '{}'\n{} = '{}'\n\n".format(dr.upper(), dr, ar.upper(), ar)
        lines.append(line)
        dr_set.add(dr)
        ar_set.add(ar)

    with open('rabbit.txt', 'w', encoding='utf8') as f:
        f.writelines(lines)




if __name__ == '__main__':
    main()
