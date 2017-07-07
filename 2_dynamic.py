#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-07 15:43:40
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
from __future__ import print_function
import os
from distutils.core import setup
from Cython.Build import cythonize


def main():
    ls = []
    for dirpath, dirname, filename in os.walk('.'):
        # print(1)
        if '__init__.py' not in filename:
            os.system('touch %s' % os.path.abspath(os.path.join(dirpath, '__init__.py')))
            print(1)
    #     for path in filename:
    #         if path.endswith('py') and not path.startswith('_'):
    #             real_path = os.path.abspath(os.path.join(dirpath, path))
    #             if 'master' in real_path or 'Setup' in real_path:
    #                 continue
    #             ls.append(os.path.abspath(real_path))
    #             # print(os.path.abspath(os.path.join(dirpath, path)))
    # setup(ext_modules=cythonize(ls))
    # # setup(ext_modules = cythonize(["/battle/workspace/battle_config.py"]))

if __name__ == '__main__':
    main()
