#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-28 18:02:03
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import pandas as pd


def main():
    for i in os.listdir('.'):
        if i.endswith('csv'):
            df = pd.read_csv(i, skiprows=[0])
            # df.drop([0], inplace=True)
            df.to_csv(i, index=False)
            

if __name__ == '__main__':
    main()